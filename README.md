# BackMix: Regularizing Open Set Recognition by Removing Underlying Fore-Background Priors 🖼️

[![Static Badge](https://img.shields.io/badge/BackMix_arXiv-PAPER-lightblue)](https://arxiv.org/abs/2503.17717)
[![Static Badge](https://img.shields.io/badge/BackMix_IEEE-PAPER-lightblue)](https://ieeexplore.ieee.org/document/10923742/)
[![Static Badge](https://img.shields.io/badge/BackMix-BLOG-lightblue)](https://vanixxz.github.io/backmix-blog/)

[![Static Badge](https://img.shields.io/badge/YouTube_(EN)-VIDEO-white)](https://www.youtube.com/watch?v=hzQH56LvuUA)
[![Static Badge](https://img.shields.io/badge/bilibili_(ZH)-VIDEO-white)](https://www.bilibili.com/video/BV1mBZVYqENv/?spm_id_from=333.337.search-card.all.click&vd_source=394f422d0ec3c4608ddb31aabb4c6461)

📖 ***IEEE TPAMI 2025***
<br>
🖋️ ***Author: Yu Wang, Junxian Mu, Hongzhi Huang, Qilong Wang, Pengfei Zhu, Qinghua Hu***

🏫 *Tianjin Key Lab of Machine Learning, College of Intelligence and Computing, Tianjin University, China*
<br>
🏛️ *Haihe Laboratory of Information Technology Application Innovation (Haihe Lab of ITAI), Tianjin, China*

## Overview
Open set recognition (OSR) requires models to classify known samples while detecting unknowns. Current methods use auxiliary datasets to regularize OSR models but are sensitive to outlier selection. We propose a new perspective: **Can we regularize OSR models without carefully chosen outliers?** Our analysis reveals that: 

1) Correlated backgrounds mislead models on 'partially' known images; 

2) Unrelated backgrounds can serve as natural outliers. 

Based on this, we propose **Background Mix (BackMix)**, which mixes image foregrounds (estimated via CAMs) with random backgrounds to break fore-background correlations. This simple yet effective method improves OSR performance without inference overhead and integrates easily with existing frameworks.


## Background Mix (BackMix)
BackMix first **estimates and masks the foreground of the background image**, then randomly **cuts patches and pastes them on the target image** to obtain the mixed image as the training sample.

<table align="center">
  <tr>
    <td align="center" width="450">
      <video 
        src="https://github.com/user-attachments/assets/f6bb9965-a852-4258-9806-f8146338b567" 
        controls 
        style="max-width:100%;">
      </video>
    </td>
  </tr>
  <tr>
    <td align="center">
      <em>Step-by-step workflow of ​​Backmix</em>
    </td>
  </tr>
</table>


## Dependencies
We train our models under ```python=3.8, pytorch=1.11, cuda=11.8```. Other versions might be available as well.

1. Install Pytorch and torchvision. Follow the instruction on https://pytorch.org/get-started/locally/.
```sh
# an example:
conda install -c pytorch pytorch torchvision
```

2. Install other needed packages (numpy, scikit-learn, etc.)


## Citation
If you find our code / paper useful in your research, please consider cite our work. 💖
```
@article{wang2025backmix,
  author={Wang, Yu and Mu, Junxian and Huang, Hongzhi and Wang, Qilong and Zhu, Pengfei and Hu, Qinghua},
  journal={IEEE Transactions on Pattern Analysis and Machine Intelligence}, 
  title={BackMix: Regularizing Open Set Recognition by Removing Underlying Fore-Background Priors}, 
  year={2025},
  pages={1-12},
  doi={10.1109/TPAMI.2025.3550703}
}
```

## Acknowledgement
We acknowledge the following repositories for providing useful components / functions in our work. 💁‍♀️

> [**ARPL**](https://github.com/iCGY96/ARPL) (*Adversarial Reciprocal Points Learning for Open Set Recognition [TPAMI'2022]*)

> [**CSSR**](https://github.com/xyzedd/CSSR) (*Class Specific Semantic Reconstruction for Open Set Recognition [TPAMI'2023]*)
