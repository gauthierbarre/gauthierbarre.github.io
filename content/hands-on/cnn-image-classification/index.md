---
title: "Deep Learning for Image Classification: From Scratch CNNs to Transfer Learning"
summary: Implementing and comparing CNN architectures using PyTorch, with data augmentation, dropout, early stopping, and transfer learning on MNIST and CIFAR-10.
topic: Deep learning
date: 2026-11-17
notebook: Lab_CNN.ipynb
---

Train a LeNet-5 convolutional network from scratch in PyTorch to classify the handwritten digits
of [MNIST](https://pytorch.org/vision/stable/generated/torchvision.datasets.MNIST.html), then
extend the same pipeline to [CIFAR-10](https://pytorch.org/vision/stable/generated/torchvision.datasets.CIFAR10.html)
and to a pre-trained ResNet18.

**What the notebook does**

- LeNet-5 with two convolutional layers (5×5 kernels, max pooling) and three fully connected
  layers `400 → 120 → 84 → 10`, with ReLU; the first convolution is padded to take 28×28 MNIST
  images.
- Inputs normalised to [−1, 1], a 50/50 split of the MNIST training set into train and validation,
  cross-entropy loss and SGD with momentum 0.9 (learning rate 0.01, weight decay 1e-6).
- The same network rewritten with `nn.Sequential`, and an early-stopping rule on the validation
  loss, both enabled by flags of a single `main()` function so the original run stays reproducible.
- A confusion matrix on the test set to see which digits are confused with which.
- For CIFAR-10: a 3-channel first layer, data augmentation (random crop with padding, horizontal
  flip) applied to the training split only, dropout in the fully connected layers, and a
  pre-trained ResNet18 whose last layer is replaced by a 10-class output.

**What it shows**

On MNIST, LeNet-5 reaches 98.95% test accuracy after 50 epochs. Training accuracy reaches 100%
while the validation loss stops improving after about ten epochs, which motivates the
early-stopping rule. The `nn.Sequential` version gives the same result (98.89% and 98.93% test
accuracy in two runs). The CIFAR-10 and ResNet18 cells are implemented but were not run in this
version of the notebook, so no results are reported for them.
