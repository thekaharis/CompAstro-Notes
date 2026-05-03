---
type: concept
title: "Vision Transformer"
created: 2026-04-14
updated: 2026-04-16
tags:
  - concept/ml
  - domain/inference
status: seed
complexity: intermediate
domain: "[[Inference and ML]]"
aliases:
  - "ViT"
related:
  - "[[SKATR]]"
  - "[[Self-Supervised Learning]]"
  - "[[Neural Posterior Estimation]]"
sources:
  - "[[Ore et al 2025 (SKATR)]]"
  - "[[Schosser et al 2025 (Starobinsky)]]"
---

# Vision Transformer

## Historical Context: Transformer Architecture

The Vision Transformer (ViT) is an adaptation of the **Transformer** architecture, introduced by Vaswani et al. (2017) in "Attention Is All You Need." The Transformer was originally developed for natural language processing (BERT, GPT) and is based on the insight that **self-attention is a more powerful and flexible primitive than convolutional or recurrent operations** for capturing global dependencies in sequential data.

### Why "Attention"?

The key innovation is the self-attention mechanism, which allows every element in a sequence to directly interact with every other element:
- **CNNs use convolution**: Each output location only sees a local neighborhood, requiring many layers to build up a global receptive field
- **RNNs use recurrence**: Information propagates sequentially, creating bottlenecks and long-term dependency challenges
- **Transformers use attention**: Every position attends to every other position simultaneously, providing an immediate global receptive field from layer 1

For 21cm data, where bubble topology is **non-local** (a large bubble at one location correlates with ionization states 10+ Mpc away due to the radiation field), the global receptive field is a natural advantage.

## Definition and Architecture

A Vision Transformer (ViT) is a neural network architecture that applies the Transformer self-attention mechanism to image or volumetric data by:

1. **Splitting the input into patches**: Dividing an image or 3D volume into fixed-size non-overlapping regions
2. **Linearizing patches**: Treating each patch as a "token," analogous to words in an NLP Transformer
3. **Applying self-attention**: Computing pairwise interactions between all patches using the Transformer mechanism
4. **Global receptive field**: The self-attention layer provides a direct connection between all patches from the first layer

## How Vision Transformers Work: The Multi-Head Attention Mechanism

### The Attention Formula

The fundamental operation in a Transformer is **scaled dot-product attention**:

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right) V$$

where:
- **Queries** ($Q = XW_Q$): A linear projection of the input embeddings $X$ with weight matrix $W_Q$
- **Keys** ($K = XW_K$): Another linear projection with weight matrix $W_K$
- **Values** ($V = XW_V$): A third linear projection with weight matrix $W_V$
- **Scaling factor** ($1/\sqrt{d_k}$): Prevents gradient vanishing in backpropagation (see below)

### Step-by-Step Computation

1. **Project input to Q, K, V**: For an input embedding $x_i$ (e.g., a patch embedding), compute
   $$q_i = W_Q x_i, \quad k_i = W_K x_i, \quad v_i = W_V x_i$$

2. **Compute attention scores**: For each pair of patches $(i, j)$, compute the dot product
   $$s_{ij} = q_i \cdot k_j^T = \left( W_Q x_i \right) \cdot \left( W_K x_j \right)^T$$
   This measures how much patch $i$ should "attend to" patch $j$: high score = high relevance.

3. **Normalize with softmax**: Apply softmax across all $j$ for each fixed $i$:
   $$\alpha_{ij} = \frac{\exp(s_{ij} / \sqrt{d_k})}{\sum_k \exp(s_{ik} / \sqrt{d_k})}$$
   This produces attention weights that sum to 1 over all patches.

4. **Weighted sum of values**: For each patch $i$, compute the output as a weighted sum of all value vectors:
   $$\text{Attn}(x_i) = \sum_j \alpha_{ij} v_j$$

### Why Dividing by $\sqrt{d_k}$ Prevents Gradient Vanishing

The dot products $q_i \cdot k_j^T$ can have large magnitude when $d_k$ (the embedding dimension) is large. If scores are too large before softmax, the softmax probabilities become sharply peaked (one $\alpha_{ij} \approx 1$, others $\approx 0$). During backpropagation, the gradient of softmax with respect to large inputs is small:

$$\frac{\partial \text{softmax}(z)}{\partial z} \approx \alpha_i (1 - \alpha_i)$$

When $\alpha_i \approx 1$, this gradient is tiny, causing **vanishing gradients**. Scaling by $1/\sqrt{d_k}$ keeps the dot products moderate (variance $\approx 1$), maintaining reasonable gradients during training.

### Multi-Head Attention

Instead of a single attention head, ViTs use **multi-head attention**: compute $h$ attention heads in parallel, each with different learned $W_Q^{(l)}, W_K^{(l)}, W_V^{(l)}$:

$$\text{MultiHead}(Q, K, V) = \text{Concat}(\text{Head}_1, \ldots, \text{Head}_h) W^O$$

where each head computes attention independently:

$$\text{Head}_l = \text{Attention}(Q W_Q^{(l)}, K W_K^{(l)}, V W_V^{(l)})$$

and $W^O$ is an output projection matrix. Multi-head attention allows the model to attend to different aspects of the data in parallel:
- Some heads might focus on local bubble boundaries
- Others might focus on large-scale ionization structure
- Others might focus on frequency correlations

Typically, $h = 8$–$16$ heads per layer, and modern ViTs stack 12–24 such layers.

## Patch Embedding for 21cm Data

### Standard 2D Image ViT

For a standard image:
- Input: $H \times W \times 3$ pixels (height × width × RGB channels)
- Patch size: $p \times p$ (typically $16 \times 16$)
- Number of patches: $N = (H/p) \times (W/p)$
- Patch embeddings: Each patch is flattened to a vector of size $p^2 \times 3$ and linearly projected to dimension $d_{\text{model}}$ (typically 768)

### 3D Volumetric ViT for 21cm Lightcones

For a 3D 21cm lightcone $(x, y, \nu)$ representing spatial and frequency dimensions:
- Input: $N_x \times N_y \times N_\nu$ voxels (e.g., $256^3$)
- Patch size: $p_x \times p_y \times p_\nu$ (e.g., $4 \times 4 \times 4$)
- Number of patches: $N = (N_x/p_x) \times (N_y/p_y) \times (N_\nu/p_\nu)$
- Patch embeddings: Each $p_x \times p_y \times p_\nu$ block is flattened to a vector of size $p_x p_y p_\nu$ and linearly projected to $d_{\text{model}}$

For a $256^3$ lightcone with $4^3$ patches:
- Number of patches: $(256/4)^3 = 64^3 = 262,144$ patches
- This is computationally expensive; many implementations use 2D slices or coarser patch sizes

## The CLS Token and Global Representation

A key component of ViTs is the **[CLS] token** (classification token):

1. **Prepend a special token**: Before processing patches, prepend a learnable embedding token $[\text{CLS}]$ to the sequence
2. **Process with all patches**: Run self-attention on the sequence $[\text{CLS}], \text{patch}_1, \text{patch}_2, \ldots, \text{patch}_N$
3. **Extract final representation**: The output embedding of the [CLS] token (after all attention layers) serves as the **global representation** of the entire input
4. **Attach downstream head**: The [CLS] embedding is fed to a linear classifier or regression head for downstream tasks

**Why this works**: During self-attention, the [CLS] token attends to all patches and aggregates information across the entire input. The final [CLS] representation thus encodes a global summary of the input.

This design is elegant because it forces the model to learn global features (attending to all patches is necessary for the [CLS] token to be useful) while keeping the architecture simple.

## Why ViTs Outperform CNNs for 21cm Data

### The Non-Local Bubble Topology Problem

In reionization simulations, ionized bubbles are generated from sources (star-forming regions) and expand outward. A crucial feature is that **bubbles at different locations are correlated on scales of 10+ Mpc** because they grow from the same ionizing background radiation field. This is a **non-local correlation**: the ionization state at position $\mathbf{x}_1$ is correlated with the state at $\mathbf{x}_2$ even if they are far apart.

### Why CNNs Struggle

**Convolutional neural networks (CNNs)** build up receptive fields hierarchically:
- Layer 1: Each neuron sees a $3 \times 3$ (or $5 \times 5$) local neighborhood
- Layer 2: By combining layer 1 outputs, a neuron sees a $7 \times 7$ neighborhood
- Layer $L$: Receptive field scales as $(2L+1)^3$ or exponentially with depth

To capture correlations at 10+ Mpc scales (equivalent to a receptive field of ~64 grid cells for a typical 21cm simulation), a CNN requires ~6–8 layers just to build up sufficient receptive field. Adding more layers for learning capacity leads to very deep networks that are:
- Slow to train
- Prone to gradient vanishing/explosion
- Prone to over-fitting on small datasets

### Why ViTs Succeed

**Vision Transformers** provide a **global receptive field from the first layer**: the self-attention mechanism directly connects all patches to each other. In the attention computation:

$$\alpha_{ij} = \text{softmax}(q_i \cdot k_j / \sqrt{d_k})$$

the softmax is computed over **all $N$ patches**, not just a local neighborhood. This means:
- A patch can attend to any other patch, regardless of distance
- The model learns which distant patches are relevant for each decision
- Global patterns (like large bubble topology) can be captured with fewer layers

In [[SKATR]], ViTs with 12 layers significantly outperform CNN baselines (ResNet, UNet-style architectures) on 21cm regression tasks, especially for cross-simulator generalization.

### Quantitative Advantage

A rough comparison:
- **CNN**: To capture 64-cell receptive field requires ~$\log_2(64) \approx 6$ layers; total parameters scale as $L \times \text{channels}^2$
- **ViT**: Global receptive field from layer 1; attention scales as $\mathcal{O}(N^2)$ in patches, but queries/keys/values are lower-dimensional ($d_k$ much smaller than image resolution), so computation per layer is modest

For 21cm data with ~1000–10000 labeled simulations:
- ViT with 12 layers, $d_{\text{model}} = 256$: ~20M parameters, trains quickly, generalizes well
- CNN with 20 layers for comparable receptive field: ~50M parameters, trains slowly, over-fits on small datasets

## Positional Encoding: Options and Choices for 21cm

### Learned Positional Embeddings

A simple approach: associate each patch with a **learnable embedding** that encodes its position:

$$x_{\text{patch}, i}^{\text{emb}} = \text{PatchEmbedding}(i) + \text{PositionalEmbedding}(i)$$

where $\text{PositionalEmbedding}(i)$ is a learned $d_{\text{model}}$-dimensional vector for patch $i$. These embeddings are trained as part of the network.

**Advantages**: Flexible, no prior assumptions about position  
**Disadvantages**: Requires learning $N \times d_{\text{model}}$ parameters; generalizes poorly to inputs with different numbers of patches (e.g., finer-resolution 21cm simulations)

### Sinusoidal Positional Encodings

The original Transformer paper uses sinusoidal functions:

$$\text{PE}(i, 2j) = \sin(i / 10000^{2j/d_{\text{model}}}), \quad \text{PE}(i, 2j+1) = \cos(i / 10000^{2j/d_{\text{model}}})$$

This encodes position information as sine/cosine waves at different frequencies. The encoding:
- **Generalizes to longer sequences**: a model trained on 1000-token sequences can handle 10000-token sequences because the sinusoidal pattern continues
- **Encodes distance information**: the distance between positions $i$ and $j$ is implicitly encoded by the difference $\text{PE}(i) - \text{PE}(j)$

**Advantages**: No parameters to learn; resolution-agnostic  
**Disadvantages**: Fixed formula may not optimally encode the structure of 21cm data

### Frequency-Aware Positional Encoding for 21cm Lightcones

A more specialized approach for 21cm data: exploit the fact that the **frequency/redshift axis is fundamentally different from spatial axes**:
- **Spatial axes** ($x$, $y$): Correspond to comoving distance in Mpc; distance is Euclidean
- **Frequency axis** ($\nu$ or redshift $z$): Corresponds to cosmic time; different frequencies sample different cosmic epochs with different ionization states

A frequency-aware encoding might:
- Use one sinusoidal pattern for spatial coordinates with period encoding ~comoving Mpc scale
- Use a different pattern for frequency coordinates that encodes the cosmic time corresponding to that frequency
- Include additional information about the sound speed or ionization timescale at that redshift

This is more specialized than standard ViT positional encoding and would require domain expertise to design. SKATR may or may not use this; the paper isn't explicit on this detail.

## Computational Complexity: O(N²) Attention

### The Quadratic Cost

The main computational bottleneck in ViTs is the self-attention mechanism. For an input with $N$ patches:

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right) V$$

- **Computing $QK^\top$**: $\mathcal{O}(N^2 d_k)$ operations (matrix multiplication $N \times d_k$ times $d_k \times N$)
- **Applying softmax**: $\mathcal{O}(N^2)$ operations
- **Computing weighted sum**: $\mathcal{O}(N^2 d_v)$ operations

**Total per attention head**: $\mathcal{O}(N^2 d_{\text{model}})$  
**Total for $L$ layers with $h$ heads**: $\mathcal{O}(L h N^2 d_{\text{model}})$

### Implications for Large 21cm Volumes

For a $256^3$ lightcone with $4^3$ patches:
- $N = 64^3 = 262,144$ patches
- A single attention operation costs $\sim 10^{12}$ floating-point operations

This is expensive, forcing a trade-off:
- **Use smaller patches** ($8^3$ per patch) → smaller $N$, faster attention, but less detail per patch
- **Use coarser input resolution** (e.g., $128^3$ instead of $256^3$) → smaller $N$, loses fine-scale structure
- **Use a hierarchical ViT** (Swin ViT) with local windows that attend only to nearby patches, reducing complexity

### Comparison to Other Architectures

- **CNN with 20 layers**: $\mathcal{O}(L N d_{\text{model}}^2)$ for convolutional operations; linear scaling with $N$
- **ViT with 12 layers**: $\mathcal{O}(12 N^2 d_{\text{model}})$; quadratic in $N$
- **Fourier Neural Operator (FNO)**: $\mathcal{O}(N \log N d_{\text{model}})$ for FFT-based operations; nearly linear

For $N = 262,144$:
- CNN: ~$10^{10}$ operations (fast)
- ViT: ~$10^{12}$ operations (slow, but global receptive field)
- FNO: ~$10^7$ operations (very fast)

ViT's quadratic cost limits it to smaller inputs (typically $N \lesssim 10^5$ patches for practical training on consumer GPUs). For very large 21cm volumes, FNO becomes more attractive, or one must use hierarchical attention (e.g., Swin ViT) to reduce complexity.

## Architectural Variants and Scaling

### ViT-Tiny, ViT-Small, ViT-Base, ViT-Large

The "size" of a ViT is determined by:
- **Number of layers** ($L$): 12–24 typically
- **Embedding dimension** ($d_{\text{model}}$): 192–1024 typically
- **Number of attention heads** ($h$): 3–16 typically

Common variants:
- **ViT-Tiny**: 12 layers, 192 dimensions, 3 heads → ~5M parameters
- **ViT-Small**: 12 layers, 384 dimensions, 6 heads → ~22M parameters
- **ViT-Base**: 12 layers, 768 dimensions, 12 heads → ~86M parameters
- **ViT-Large**: 24 layers, 1024 dimensions, 16 heads → ~307M parameters

### Choosing ViT Size for 21cm

For [[SKATR]], which has ~10,000 labeled simulations available for downstream fine-tuning, the optimal choice is likely:
- **ViT-Small or ViT-Base**: 20–86M parameters
- Larger models (ViT-Large) risk over-fitting on the small labeled dataset
- Smaller models (ViT-Tiny) may not have enough capacity to capture complex 21cm structure

This is similar to the rule-of-thumb in computer vision: use models with 10–100 million parameters for datasets with 10,000–100,000 labeled examples. Going much larger requires data augmentation, regularization, or unsupervised pre-training.

## Advantages of ViTs Over CNNs for 21cm (Detailed)

### 1. Global Receptive Field

CNNs require many layers to build global context; ViTs have it from layer 1. For 21cm fields where bubble correlations span 10+ Mpc, this is a huge advantage.

### 2. Better Generalization to New Resolutions

A CNN trained on $128^3$ data performs poorly on $256^3$ data (the receptive field relative to the input size is different). A ViT trained on patches scales more gracefully because the patch size is fixed, and attention operates on patch tokens uniformly.

### 3. Cleaner Inductive Bias

CNNs have a strong inductive bias: local interactions (convolution) are prioritized. This is reasonable for natural images but not for 21cm fields where non-local correlations matter. ViTs have a weaker (more flexible) inductive bias, allowing the model to learn task-specific attention patterns.

### 4. Better Cross-Simulator Transfer

In [[SKATR]], self-supervised ViT pre-training generalizes better to different simulators than supervised CNN training. This likely reflects that ViTs capture global, physics-based patterns (bubble topology) while CNNs over-fit to local simulator artifacts.

## Connections to This Thesis

- **[[SKATR]]**: Uses a ViT backbone (likely ViT-Small or ViT-Base) with self-supervised contrastive pre-training for parameter regression on 21cm fields
- **[[Schosser et al 2025 (Starobinsky)]]**: Uses ViTs as neural summary networks for simulation-based inference, outperforming CNN and power-spectrum baselines
- **Broader motivation**: The success of ViTs in 21cm applications supports the hypothesis that **global attention is the right architectural primitive for cosmological fields** with non-local correlations

ViTs represent the current state-of-the-art in ML for cosmological field data, positioned between lower-cost traditional approaches (power spectrum statistics, CNN features) and higher-cost methods that operate directly on fields (FNOs, emulators). The global receptive field and good generalization properties make ViTs particularly valuable for this thesis's goal of robust, simulator-independent inference.
