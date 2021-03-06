# Knowledge_distillation_via_TF2.0
- The codes for recent knowledge distillation algorithms and benchmark results via TF2.0 low-level API.
- I implemented all of the algorithms using TF2.0 as a lower API as possible.
- This Repo. will be upgraded version of my previous benchmark Repo. ([link](https://github.com/sseung0703/KD_methods_with_TF))
- Also, this Repo. provides low-level implemented codes for
  - famous neural layers such as Convolutional, Fully-connected, Dropout, and Batchnorm,
  - a custom model which contain argscope which acts just same with TF1.x,
  - Custom training loop for a teacher-student network with learning rate scheduler,
- The codes are not optimal yet but work well. I'll improve them soon.
  
# Implemented Knowledge Distillation Methods
Please check detail of each category in [MHGD](https://arxiv.org/abs/1907.02226) and If you think the above categorization is useful, please consider citing the following paper.

    @inproceedings{GraphKD,
      title = {Graph-based Knowledge Distillation by Multi-head Attention Network},
      author = {Seunghyun Lee, Byung Cheol Song},
      booktitle = {British Machine Vision Conference (BMVC)},
      year = {2019}
    }

## Response-based Knowledge (nets/Response.py)
Defined knowledge by the neural response of the hidden layer or the output layer of the network
- Soft-logit : The first knowledge distillation method for deep neural network. Knowledge is defined by softened logits. Because it is easy to handle it, many applied methods were proposed using it such as semi-supervised learning, defencing adversarial attack and so on.
  - [Geoffrey Hinton, et al. Distilling the knowledge in a neural network. arXiv:1503.02531, 2015.](https://arxiv.org/abs/1503.02531)
- Deep Mutual Learning (DML) : train teacher and student network coincidently, to follow not only training results but teacher network's training procedure.
  - [Zhang, Ying, et al. "Deep mutual learning." Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition. 2018.](http://openaccess.thecvf.com/content_cvpr_2018/html/Zhang_Deep_Mutual_Learning_CVPR_2018_paper.html) (on worning)
- Factor Transfer (FT) : Encode a teacher network's feature map, and transfer the knowledge by mimicking it.
  - [Jangho Kim et al. "Paraphrasing Complex Network: Network Compression via Factor Transfer" Advances in Neural Information Processing Systems (NeurIPS) 2018](https://papers.nips.cc/paper/7541-paraphrasing-complex-network-network-compression-via-factor-transfer) (on worning)

## Multi-connection Knowledge (nets/Response.py)
Increase the quantity of knowledge by sensing several points of the teacher network
- FitNet : To increase amounts of information, knowledge is defined by multi-connected networks and compared feature maps by L2-distance.
  - [Adriana Romero, et al. Fitnets: Hints for thin deep nets. arXiv preprint arXiv:1412.6550, 2014.](https://arxiv.org/abs/1412.6550)
- Attention transfer (AT) : Knowledge is defined by attention map which is L2-norm of each feature point.
  - [Zagoruyko, Sergey et. al. Paying more attention to attention: Improving the performance of convolutional neural networks via attention transfer. arXiv preprint arXiv:1612.03928, 2016.](https://arxiv.org/pdf/1612.03928.pdf) [[the original project link](https://github.com/szagoruyko/attention-transfer)]
- Activation boundary (AB) : To soften teacher network's constraint, they propose the new metric function inspired by hinge loss which usually used for SVM.
  - [Byeongho Heo, et. al. Knowledge transfer via distillation of activation boundaries formed by hidden neurons. AAAI2019](https://arxiv.org/abs/1811.03233) (rivised by Author) [[the original project link](https://github.com/bhheo/AB_distillation)]
- VID : Define variational lower boundary as the knowledge, to maximize mutual information between teacher and student network. 
  - [Ahn, et. al. Variational Information Distillation for Knowledge Transfer](http://openaccess.thecvf.com/content_CVPR_2019/papers/Ahn_Variational_Information_Distillation_for_Knowledge_Transfer_CVPR_2019_paper.pdf) (on worning)

## Shared-representation Knowledge (nets/Response.py)
Defined knowledge by the shared representation between two feature maps
- Flow of Procedure (FSP) : To soften teacher network's constraint, they define knowledge as relation of two feature maps.
  - [Junho Yim, et. al. A gift from knowledge distillation:
Fast optimization, network minimization, and transfer learning. CVPR 2017.](http://openaccess.thecvf.com/content_cvpr_2017/html/Yim_A_Gift_From_CVPR_2017_paper.html)
- KD using Singular value decomposition(KD-SVD) : To extract major information in feature map, they use singular value decomposition.
  - [Seung Hyun Lee, et. al. Self-supervised knowledge distillation using singular value decomposition. ECCV 2018](http://openaccess.thecvf.com/content_ECCV_2018/html/SEUNG_HYUN_LEE_Self-supervised_Knowledge_Distillation_ECCV_2018_paper.html) [[the original project link](https://github.com/sseung0703/SSKD_SVD)]

## Relational Knowledge (nets/Response.py)
Defined knowledge by intra-data relation
- Relational Knowledge Distillation (RKD): they propose knowledge which contains not only feature information but also intra-data relation information.
  - [Wonpyo Park, et. al. Relational Knowledge Distillation. CVPR2019](https://arxiv.org/abs/1904.05068?context=cs.LG) [[the original project link](https://github.com/lenscloth/RKD)]
- Multi-head Graph Distillation (MHGD): They proposed the distillation module which built with the multi-head attention network. 
Each attention-head extracts the relation of feature map which contains knowledge about embedding procedure.
  - [Seunghyun Lee, Byung Cheol Song. Graph-based Knowledge Distillation by Multi-head Attention Network. will be published in BMVC2019](https://arxiv.org/abs/1907.02226) [[the original project link](https://github.com/sseung0703/MHGD)]
  
# Experimental Results
The below table and plot are sample results using WResNet and train on CIFAR100.

I use the same hyper-parameter for training each network, and only tune hyper-parameter of each distillation algorithm. However the results may be not optimal. All of the numerical values and plots are averages of five trials.

## Network architecture
The teacher network is WResNet40-4 and Student is WResNet16-4, and the student network is well-converged (not over and under-fit) for evaluating each distillation algorithm performance precisely.

## Training/Validation accuracy
(* means that it looks working well but need more check)

|             |  Full Dataset |  50% Dataset  |  25% Dataset  |  10% Dataset  |
|:-----------:|:-------------:|:-------------:|:-------------:|:-------------:|
|   Methods   | Accuracy | Last Accuracy | Last Accuracy | Last Accuracy |
|   Teacher   |         77.80 |       -       |       -       |       -       |
|   Student   |         76.37 |         70.09 |         62.56 |         43.60 |
| Soft_logits |         76.77 |         70.91 |         62.93 |         43.89 |
|   FitNet*   |         74.91 |         67.82 |         61.11 |         43.01 |
|      AT     |         77.55 |         72.00 |         64.71 |         49.03 |
|     FSP*    |         73.15 |         67.25 |         58.86 |         41.03 |
|     DML     |               |               |               |               |
|    KD_SVD   |         76.85 |         72.70 |         66.91 |         53.00 |
|    KD_EID   |         77.22 |         72.81 |         66.54 |         54.27 |
|      FT     |               |               |               |               |
|      AB     |         76.57 |         71.79 |         66.88 |         56.72 |
|     RKD*    |         76.57 |         71.10 |         61.63 |         33.01 |
|     VID     |               |               |               |               |
|     MHGD    |         77.23 |         72.94 |         67.31 |         51.97 |

# Plan to do
- Converting TF1.x algorithm to TF2.0. ( 10 / 12 )
- Final check for KD algorithm is on going.( 9 / 12 )


