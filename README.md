# finetune-anything

## Introduction

The [Segment Anything Model (SAM)](https://github.com/facebookresearch/segment-anything) has revolutionized computer vision. Relying on fine-tuning of SAM will solve a large number of basic computer vision tasks. We are designing a **class-aware one-stage** tool for training fine-tuning models based on SAM. 

You need to supply the datasets for your tasks and the [supported task](#Supported-Tasks) name, this tool will help you to get a finetuned model for your task.

<img width="640" src="https://user-images.githubusercontent.com/67993288/230864865-db8810fd-9f0c-4f3e-81b1-8753b5121d03.png">

## Install
### Step1
```
git clone https://github.com/ziqi-jin/finetune-anything.git
cd finetune-anything
pip install -r requirements.txt
```
### Step2
Download the SAM weights from [SAM repository](https://github.com/facebookresearch/segment-anything#model-checkpoints)

### Step3
Modify the contents of yaml file for the specific task in **/config**, e.g., ckpt_path, model_type ...

## Supported Tasks
- [x] Semantic Segmentation
    - [x] train
    - [x] eval
    - [ ] test
- [ ] Matting
- [ ] Instance Segmentation
- [ ] Detection 
## Supported Datasets
- [x] TorchVOCSegmentation
- [ ] BaseSemantic
- [ ] BaseInstance
- [ ] BaseMatting
## Train
```
CUDA_VISIBLE_DEVICES=${your GPU number} python train.py --task_name semantic_seg
```
## Test

## Deploy

- [ ] Onnx export
