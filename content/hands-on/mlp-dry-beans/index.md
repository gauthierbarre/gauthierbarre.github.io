---
title: "Training an MLP in PyTorch, and when to stop"
summary: A multi-layer perceptron written from scratch in PyTorch on the Dry Bean dataset, from preprocessing to early stopping.
topic: Deep learning
date: 2026-11-17
source: "Télécom Paris · deep learning lab"
notebook: Lab_MLP.ipynb
---

A deep learning lab from Télécom Paris: train and evaluate a multi-layer perceptron for a
7-class classification problem on the public [Dry Bean dataset](https://archive.ics.uci.edu/dataset/602/dry+bean+dataset)
(13,611 beans, 16 shape features). I wrote every line of code myself, using AI only to ask
questions and understand concepts.

**What the notebook does**

- Preprocessing with pandas and scikit-learn: label encoding, an 80/20 train/validation split,
  and a scaler fitted on the training set only, to avoid leakage.
- A PyTorch `Dataset` and `DataLoader`, then an MLP `16 → 128 → 64 → 64 → 7` with ReLU,
  trained with cross-entropy and Adam (learning rate 0.001).
- A training loop that tracks loss and accuracy on both sets at every epoch.

**What it shows**

Validation accuracy reaches about 93% within ten epochs and then stays flat, while the training
loss keeps falling. Over 100 epochs the validation loss rises from about 0.19 to 0.23: the model
starts to overfit. An early-stopping rule (stop after 5 epochs without a new minimum of the
validation loss) ends training at epoch 17. One question is left open at the end: whether to keep
the last weights or those at the minimum of the validation loss.
