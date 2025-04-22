import os
import time
import torch
import numpy as np
import torch.nn as nn
import torch.utils.data as data
import torch.nn.functional as F

from torchvision import transforms

class BMixDataset(data.Dataset):
    def __init__(self, src_ds):
        self.aug = transforms.Compose([transforms.RandomHorizontalFlip(), transforms.RandomCrop(size = 32, padding = int(32*0.125))])
        self.resize_crop = transforms.Compose([transforms.Resize(32), transforms.CenterCrop(32)])
        self.totensor = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.25, 0.25, 0.25))])
        self.topil = transforms.ToPILImage()
        self.seg_momemtum = 0.1        
        self.seg_bank = None                                
        self.enabled_mask = False
        self.ds = src_ds
        self.init_segbank(8, 8)
    
    
    def __len__(self, ):
        return len(self.ds)
    
    
    def init_segbank(self, h, w):
        self.seg_bank = torch.ones([len(self.ds), h, w])*0.5


    def soft_seg(self, idx, seg_mask):
        _, h, w = seg_mask.shape
        if self.seg_bank is None:
            self.init_segbank(h, w)
        self.seg_bank[idx] = seg_mask*self.seg_momemtum+self.seg_bank[idx]*(1-self.seg_momemtum)
    
    
    def mask_random(self, defined_size): 
        h, w = defined_size[1], defined_size[0]
        bbox_y1 = np.random.randint(0, 32-h)
        bbox_x1 = np.random.randint(0, 32-w)
        bbox_y2 = min(32, bbox_y1+h)
        bbox_x2 = min(32, bbox_x1+w)        
        return int(bbox_x1), int(bbox_x2), int(bbox_y1), int(bbox_y2)


    def __getitem__(self, idx):        
        img, lb, _ = self.ds[idx]
        img = self.resize_crop(img)
        
        def mask_highestK(seg_map, ratio, is_rand = False, interpolate = True):
            
            prob_map = seg_map.view(-1)
            prob_map /= prob_map.sum()
            
            if is_rand:
                cpu_prob = prob_map.numpy()
                prob_idx = np.random.choice(cpu_prob.shape[0], int(ratio*cpu_prob.shape[0]), False, cpu_prob)
            
            else:
                prob_idx = torch.argsort(prob_map, descending = True)[:int(ratio*prob_map.shape[0])]
                
            seg_temp = torch.zeros(prob_map.shape[0])
            seg_temp[prob_idx] = 1
            res = seg_temp.reshape(seg_map.shape).unsqueeze(0).unsqueeze(0)
            
            if interpolate:
                return F.interpolate(res, (32, 32))[0]
            else:
                return res[0]
            
        img = self.totensor(img)
        raw_img = img.detach().clone()
        bbox_x1, bbox_x2, bbox_y1, bbox_y2 = self.mask_random((0.25*32, 0.25*32))
        
        aux_idx = np.random.randint(len(self.ds))
        aux_img, _, _ = self.ds[aux_idx]
        aux_mask = mask_highestK(self.seg_bank[aux_idx], 0.25)
        aux_img = self.totensor(self.resize_crop(aux_img))
        aux_img *= 1-aux_mask
        aux_x1, aux_x2, aux_y1, aux_y2 = self.mask_random((bbox_x2-bbox_x1, bbox_y2-bbox_y1))
        
        img[:, bbox_y1:bbox_y2, bbox_x1:bbox_x2] = aux_img[:, aux_y1:aux_y2, aux_x1:aux_x2]
            
        f_img = self.topil(torch.clamp(img*0.25+0.5, 0, 1))
        mix_img = self.totensor(self.aug(f_img))            
        
        return raw_img, mix_img, lb, idx