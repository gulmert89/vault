# Study 1: Generative AI with Large Language Models
## 1. Week One: Generative AI use cases, project lifecycle, and model pre-training
* Learning Objectives
    * Discuss model pre-training and the value of continued pre-training vs fine-tuning
    * Define the terms Generative AI, large language models, prompt, and describe the transformer architecture that powers LLMs
    * Describe the steps in a typical LLM-based, generative AI model lifecycle and discuss the constraining factors that drive decisions at each step of model lifecycle
    * Discuss computational challenges during model pre-training and determine how to efficiently reduce memory footprint
    * Define the term scaling law and describe the laws that have been discovered for LLMs related to training dataset size, compute budget, inference requirements, and other factors.
### 1.1. Introduction to LLMs and the generative AI project lifecycle
#### 1.1.1. LLM use cases & tasks
* Essay Writer
* Summarize
* Translate (Sentence to sentence)
* Code generator
* Entity Extraction (NER)
* Information retrieval (with API queries)
#### 1.1.2. Text Generation before Transformers
* Before transformers (RNN, LSTM, GRU etc.), it was hard to solve such ambiguities:
    * ``Syntactic ambiguity``: "The teacher taught the students with the book."
        * Did the teacher teach using the book,
        * or did the student have the book, or was it both?
* Transformers
    * Scale efficiently
    * Parallel process
    * Attention to input meaning
* ``Attention is all you need`` paper proposes a neural network architecture that replaces traditional recurrent neural networks (RNNs) and convolutional neural networks (CNNs) with an entirely attention-based mechanism.
#### 1.1.3. Transformers architecture
* Here's a summarized version of how Transformers work in basic steps:
1. **Tokenization:** Convert input text into tokens.
2. **Embedding:** Represent each token as a d_model-dimensional vector.
3. **Positional Encoding:** Add positional information to embeddings.
4. **Self-Attention:** Compute attention scores for each token based on its relationship with all other tokens.
5. **Aggregation:** Combine token representations using attention scores.
6. **Feed-Forward Networks:** Pass aggregated vectors through feed-forward neural networks.
7. **Layer Normalization & Residual Connection:** Normalize outputs and add them to the original inputs.
8. **Stacking:** Repeat the self-attention and feed-forward steps for multiple layers.
9. **Output:** Produce a sequence for sequence-to-sequence tasks or a pooled representation for classification tasks.
10. **Final Layer:** Depending on the task, transform the output using a linear layer followed by a task-specific activation function (e.g., softmax for classification).
* **Note:** For models like BERT, only the encoder part of the Transformer is used. For models like GPT, only the decoder part is used. The original Transformer model, as introduced in the "Attention Is All You Need" paper, uses both encoders and decoders for sequence-to-sequence tasks like translation.
#### 1.1.4. Generating text with transformers
* In the encoder only models (e.g. BERT), we can still use sequence-to-sequence tasks but the output length has to be the same as the input length.
* However, in the encoder-decoder models (e.g. BART, T5), the output length could be different than the input length.
* In the decoder only models (e.g. GPT, BLOOM, LLaMA), generate sequences from scratch or conditioned on some provided input. Generalize tasks well.
#### 1.1.5. Prompting and prompt engineering
* **In-context learning (ICL)**: Providing examples in the context window (prompt) so that the model grasps the idea what we are trying to convey. It has three types of inferences:
    * Zero shot inference
    * One shot inference
    * Few shot inference
* One shot inference involves providing an example question with answer followed by a second question to be answered by the LLM.  Few shot inference provides multiple example prompts and answers while zero shot provides only one prompt to be answered by the LLM.
#### 1.1.6. Generative configurations
* The upcoming inference parameters are not learned parameters in the training! They are invoked at the inference step.
* **Max new tokens:** Limits the maximum number for tokens inferenced.
* ***Greedy vs. Random Sampling:*** The word/token with the highest probability is selected on greedy sampling. In the random(-weighted) sampling, the tokens will be selected according to their probability score, not the highest score strictly. So, the $3^{rd}$ predicted token with $4.7\%$ probability could be selected as well even though the chances are lower. To limit the random sampling to create more meaningful but less random outputs, we have these parameters:
    * **Sample top k:** Select a sample among the top $k$ samples with the highest probability.
    * **Sample top p:** Select a sample among the top ranked consecutive results by probability and *with a cumulative probability* $<=p$.
        * Again, don't forget: ``cumulative probability!``
* **Temperature:** Changes the shape of the probability distribution the model calculates for the next token. Here is a passage from GPT-4:
    ***
    ### The Temperature Parameter in Language Models (LLMs)
    The temperature parameter in LLMs is a hyperparameter utilized during the softmax operation to control the randomness of the model's outputs.
    #### 1. **Softmax Operation**:
    When a language model produces logits (raw prediction scores) for each possible next token, these logits are transformed into a probability distribution using the softmax function:

    $\large P(i) = \frac{e^{z_i}}{\sum_j e^{z_j}}$

    Here, $P(i)$ is the probability of token $ i $, and $ z_i $ is its corresponding logit.
    #### 2. **Temperature**:
    Before the logits undergo the softmax function, they can be scaled using a temperature $ T $. The updated equation becomes:

    $\large P(i) = \frac{e^{z_i/T}}{\sum_j e^{z_j/T}}$

    The temperature $ T $ adjusts the distribution as follows:
    - $ T = 1 $: The original distribution remains unchanged.
    - $ T > 1 $: The distribution becomes "softer" or "flatter," leading to ***more randomness*** _(i.e. more creative)_ in the model's outputs.
    - $ T < 1 $: The distribution becomes "sharper," and the model becomes ***more deterministic*** in its outputs.
    #### 3. **Visualizing the Effect**:
    Consider a hypothetical scenario:
    - Let's assume for a particular context, the model produces logits: $ z_1=2, z_2=1, z_3=0 $.
    - Without temperature i.e., $ T=1 $, the probabilities might look like: $ P_1=0.67, P_2=0.24, P_3=0.09 $.
    - With a higher temperature, $ T=2 $, the probabilities become closer: $ P_1=0.44, P_2=0.33, P_3=0.23 $.
    - With a lower temperature, $ T=0.5 $, the probabilities are more skewed towards the top choice: $ P_1=0.88, P_2=0.11, P_3=0.01 $.

    If you visualize these probabilities, the bars will appear distinct without temperature, more evenly sized with a higher temperature, and highly skewed with a lower temperature.

    In summary, the temperature parameter is crucial when sampling from language models, offering a balance between randomness (exploration) and adhering to the most likely outputs (exploitation).
    ***
* As far as I understand, this is meaningful when `random sampling` takes place. When it's a greedy choice, the model picks the highest probability anyway no matter what the distribution indicates since the weighted probabilities don't affect the order.
![./assets/temperature_config.png](https://github.com/gulmert89/studyRoom_generative/blob/bbdafd4e023bbb1d4a73a0b2ab0a9d412b1ec9fc/llms/assets/temperature_config.png?raw=true)
#### 1.1.7. Generative AI project lifecycle
* Define your task first: Essay writing, summarization, translation, information retrieval, invoke APIs and actions etc.
* Lifecycle:
    * Define scope
    * Select model
        * Pretrained or train your own
    * Adapt and align model
        * Prompt engineering
        * Fine-tuning
        * Align with human feedback
        * Evaluate
    * Application integration
        * Optimize & deploy
        * Augment the model to your usage, limitations etc.
### 1.2. LLM pre-training and scaling laws
#### 1.2.1. Pre-training large language models
* There are petabytes of data on the internet. When a _data quality filter_ is applied, there could be 1-3% of the original tokens left.
* **Encoder-only (a.k.a. autoencoding) models**
    * Masked Language Modeling (MLM)
        * `The teacher <MASK> the student...`
    * **Objective:** Reconstruct text ("denoising")
        * `The teacher |teaches| the student...`
        * ``----> |bidirectional context| <----``
    * Good use cases:
        * Sentiment analysis
        * NER
        * Word classification
    * Example models: BERT, ROBERTA
* **Decoder-only (a.k.a. autoregressive) models**
    * Causal Language Modeling (CLM)
        * `The teacher ?`
    * **Objective:** Predict next token
        * `The teacher |teaches|`
        * `----> |unidirectional context|`
    * Good use cases:
        * Text generation
        * Other emergent behavior (depends on model size)
    * Example models: GPT, BLOOM
* **Encoder-Decoder models (sequence-to-sequence) models**
    * Span Corruption
        * `The teacher <MASK> <MASK> student`
        * `The teacher <X> student` where `<X>` is _sentinel token_.
    * **Objective:** Reconstruct span
        * `<X> teaches the`
    * Good use cases:
        * Translation
        * Text summarization
        * Question answering
    * Example models: T5, BART
#### 1.2.2. Computational challenges of training LLMs
* CUDA: Compute Unified Device Architecture
* GPU RAM computation:
    * $1~parameter = 4~bytes~(32$-$bit~float) $
    * $1B~parameters = 4*10^9~bytes = 4GB$
        * 4GB @ 32-bit full precision

    ||Bytes per parameter|
    |:-|:-:|
    |Model Parameters (Weights) | 4 bytes per parameter|
    |Adam optimizer (2 states)|+8 b.p.p.|
    |Gradients|+4 b.p.p.|
    |Activations and <br>temporary memory|+8 b.p.p. (high-end estimate)|
    |**TOTAL**|$=4~b.p.p. + {\scriptsize\sim}20~extra~b.p.p.$|
    * So, while we need 4GB memory to store the model, counting all these overhead in the training, we actually need ~80GB of memory (a single _Nvidia A100 GPU_ for instance) to train the model.
* There are techniques to reduce the memory required.
* **Quantization:** Reducing required memory to store and train models by projecting numbers into lower precision _(a.k.a. mantissa/significand)_ spaces (e.g. ``FP32`` to `BFLOAT16`).
    ||Bits|Exponent|Fraction|Memory needed<br>to store one value|
    |:-|:-:|:-:|:-:|:-:|
    |**FP32**|32|8|23|4 byte|
    |**FP16**|16|5|10|2 byte|
    |**BFLOAT16**|16|8|7|2 byte|
    |**INT8**|8|-|7|1 byte|
    * Oh, by the way, remember that:
    <br>![.\assets\fp-basics.jpg](https://raw.githubusercontent.com/gulmert89/studyRoom_generative/main/llms/assets/fp-basics.jpg)
    * Projects original 32-bit floating point numbers into lower precision space.
    * Quantization-aware training (QAT) learns the quantization scaling factors during training.
    * ``BFLOAT16``/`BF16` is a popular choice (`B` stands for _brain_ which refers to ***Google Brain*** team).
        * BF16 significantly helps with training stability and is supported by newer GPU's such as NVIDIA's A100, as it captures the full dynamic range of the full 32-bit float, that uses only 16-bits.
        * Not good at calculating integers but it's rare in deep learning anyway.
#### 1.2.3. Efficient multi-GPU compute strategies
* **Q:** Which of the following best describes the role of data parallelism in the context of training Large Language Models (LLMs) with GPUs?
    * Data parallelism allows for the use of multiple GPUs to process different parts of the same data simultaneously, speeding up training time. It is a strategy that splits the training data across multiple GPUs. Each GPU processes a different subset of the data simultaneously, which can greatly speed up the overall training time.
* Either your model is too big to fit in a single GPU, or your dataset is very large and you want to distribute it to multiple GPUs and train them in parallel to save time.
* ``Distributed Data Parallel (DDP)``
    * Dataloader splits the data,
    * Sends them to multiple GPUs,
    * Each one of them has their own forward/backward pass operations,
    * The gradients are ***synchronized***,
    * Each model in these separate GPUs gets updated.
        * Note that in DDP, your model (model weights, gradients, optimizer states and all the other parameters) fits onto a single GPU.
* **Model Sharding**
    * One of the popular implementations is ***Pytorch's Fully Sharded Data Parallel (FSDP)*** 
        * [PyTorch FSDP paper](https://arxiv.org/abs/2304.11277) is motivated by the ["ZeRO" paper](https://arxiv.org/abs/1910.02054) - zero data overlap between GPUs.
    * In DDP, there are one full copy of model and training parameters on each GPU.
    * In **Zero Redundancy Optimizer (ZeRO)**, the memory is reduced by distributing (sharding) the model parameters, gradients and optimizer states across GPUs.
        * ZeRO Stage 1: Only optimizer states are sharded (not the parameters and gradients. Each GPU has them all). This reduces memory footprint by up to a factor of 4.
        * ZeRO Stage 2: Also shards the gradients. Reduces memory up to 8 times.
        * ZeRO Stage 3: Shards model parameters as well. Since everything is sharded across GPUs, memory consumption is linear with the number of GPUs.
    * Each GPU requests data (weights etc.) from other GPUs on-demand to materialize the sharded data into unsharded data for the duration of the operation. After the operation, it's sent back to other GPUs.
    * 
