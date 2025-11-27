# Seeds Classification with Multi-Layer Perceptron

Machine Learning project for wheat seed classification using geometric features and neural networks.

## 📊 Project Overview

This project implements a Multi-Layer Perceptron (MLP) to classify three varieties of wheat (Kama, Rosa, and Canadian) based on seven geometric features obtained through soft X-ray imaging.

**Final Model Performance:** 99.91% ± 0.07% accuracy (K-Fold Cross-Validation)

## 🎯 Key Features

- **Automated Data Loading**: Direct download from UCI Repository
- **Robust Preprocessing**: StandardScaler normalization + Noise injection augmentation
- **Optimized Architecture**: 7→64→32→3 MLP with Dropout regularization
- **Rigorous Validation**: 5-Fold Cross-Validation for reliable performance estimation
- **Production Ready**: High accuracy with excellent stability (CV < 1%)

## 📁 Dataset

**Source:** [UCI Machine Learning Repository - Seeds Dataset](https://archive.ics.uci.edu/dataset/236/seeds)

- **Samples:** 210 (70 per class)
- **Features:** 7 geometric measurements
- **Classes:** 3 wheat varieties
- **Citation:** Charytanowicz, M., et al. (2010). Seeds [Dataset]. UCI Machine Learning Repository.

### Features

1. Area
2. Perimeter
3. Compactness (C = 4πA/P²)
4. Length of kernel
5. Width of kernel
6. Asymmetry coefficient
7. Length of kernel groove

## 🚀 Quick Start

### Prerequisites

```bash
pip install pandas numpy scikit-learn tensorflow matplotlib seaborn
```

### Running the Notebook

1. Open `Turnin/notebook/Seeds_ML_FINALPRJ_NF1002000.ipynb`
2. Run all cells sequentially
3. Dataset will be automatically downloaded from UCI Repository

## 🧠 Model Architecture

```
Input (7 features)
    ↓
Dense(64) → ReLU → Dropout(0.2)
    ↓
Dense(32) → ReLU → Dropout(0.2)
    ↓
Dense(3) → Softmax
```

**Total Parameters:** 2,691 (all trainable)

## 📈 Results

### Final Model Performance (K-Fold CV)

| Metric                   | Value             |
| ------------------------ | ----------------- |
| Mean Accuracy            | 99.91%            |
| Std Deviation            | 0.07%             |
| Coefficient of Variation | 0.07%             |
| 95% Confidence Interval  | [99.77%, 100.00%] |

### Key Techniques Applied

- **Preprocessing**: StandardScaler, Noise Injection (σ=0.02)
- **Architecture**: MLP with 2 hidden layers
- **Regularization**: Dropout (0.2) + Early Stopping (patience=15)
- **Optimization**: Adam optimizer, Batch Size=16
- **Validation**: Stratified 5-Fold Cross-Validation

## 📊 Pipeline Summary

1. **Data Loading** → Direct download from UCI Repository
2. **Preprocessing** → Scaling + Augmentation
3. **Model Design** → MLP (7→64→32→3)
4. **Training** → 100 epochs with early stopping
5. **Hyperparameter Tuning** → Dropout comparison (0.2 vs 0.4)
6. **Validation** → 5-Fold Cross-Validation

## 📝 Project Structure

```
MLFINAL/
├── Turnin/
│   ├── notebook/
│   │   └── Seeds_ML_FINALPRJ_NF1002000.ipynb  # Main notebook (final submission)
│   ├── Project Report/                         # Project documentation
│   └── VerificationVideo/                      # Video demonstration
├── DATASET/
│   └── seeds/
│       └── seeds_dataset.txt                   # Local backup
├── Rubrics_n_Requirements/                     # Assignment guidelines
├── bkp/                                        # Backup versions
├── README.md                                   # This file
└── .gitignore                                  # Git ignore rules
```

## 🎓 Course Information

**Course:** Fall 2025 Machine Learning (DAMO-640-10)  
**Student:** Fabio dos Santos Prumucena (NF100200)  
**Professor:** Ahmed Eltahawi  
**Institution:** GUSCanada

## 📄 License

This dataset is licensed under a Creative Commons Attribution 4.0 International (CC BY 4.0) license.

## 🔗 Links

- **GitHub Repository:** [https://github.com/prumucena1979/MLFINAL](https://github.com/prumucena1979/MLFINAL)
- **UCI Dataset:** [https://archive.ics.uci.edu/dataset/236/seeds](https://archive.ics.uci.edu/dataset/236/seeds)

## 🙏 Acknowledgments

- UCI Machine Learning Repository for providing the dataset
- Original dataset creators: M. Charytanowicz, J. Niewczas, P. Kulczycki, et al.
- Institute of Agrophysics, Polish Academy of Sciences

---

**Note:** This project demonstrates a complete machine learning pipeline from data acquisition to model validation, achieving state-of-the-art performance on the Seeds classification task.
