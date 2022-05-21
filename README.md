# Master's Thesis: Multilingual G2P

For my master's thesis I worked on a multilingual model for grapheme-to-phoneme conversion. 
The text group of the Language and Space lab at the University of Zurich maintains a
[project](https://www.spur.uzh.ch/en/departments/research/textgroup/MorphDiv.html) that provides a multilingual corpus consisting of 100 language text samples.
I used a subset of these languages to perform G2P experiments. Currently I am working with the following languages:

| ISO396-3 | Language            |
|----------|---------------------|
| cmn      | Chinese             |
| deu      | German              |
| ell      | Greek (Modern)      |
| eng      | English (UK and US) |
| eus      | Basque              |
| fin      | Finnish             |
| fra      | French              |
| hin      | Hindi               |
| ind      | Indonesian          |
| jpn      | Japanese (Hiragana) |
| kat      | Georgian            |
| kor      | Korean              |
| mya      | Burmese             |
| rus      | Russian             |
| spa      | Spanish             |
| tgl      | Tagalog             |
| tha      | Thai                |
| tur      | Turkish             |
| vie      | Vietnamese          |
| zul      | Zulu                |

## Results
These are the results for all of my models trained on each data type (original data: BS, preprocessed and cleaned data: BS-clean and data enriched with phonetic features: F2. The best performance is marked in bold.

| ISO 639-3 | Type WikiPron | WER BS | PER BS | WER BS-clean | PER BS-clean | WER F2 | PER F2 |
|---|---|---|---|---|---|---|---|
| cmn | broad | 17.6 | 3.9 | **17.0** | 4.0 | 18.1 | 4.4 |
| deu | broad | **37.1** | 4.8 | 38.1 | 5.0 | 38.6 | 5.9 |
| deu | narrow | **52.2** | 7.1 | 56.9 | 8.4 | 55.9 | 9.4 |
| ell | broad | **7.1** | 0.6 | 9.0 | 0.7 | 9.1 | 0.8 |
| eng us | broad | **50.7** | 9.5 | 51.2 | 10.2 | 51.3 | 10.4 |
| eng us | narrow | 84.6 | 31.4 | **84.2** | 33.1 | 84.9 | 32.3 |
| eng uk | broad | **45.5** | 8.6 | 47.5 | 9.2 | 47.6 | 9.7 |
| eng uk | narrow | **90.3** | 30.2 | 94.8 | 35.3 | 93.7 | 34.2 |
| eus | broad | 21.2 | 2.7 | **19.6** | 2.3 | 21.7 | 3.2 |
| fin | broad | **2.8** | 0.2 | 3.3 | 0.3 | 8.9 | 3.1 |
| fin | narrow | **3.2** | 0.3 | 3.9 | 0.4 | 9.0 | 3.5 |
| fra | broad | **5.3**| 0.7 | 5.8 | 0.8 | 5.9 | 0.8 |
| hin | narrow | **7.7** | 1.2 | 8.4 | 1.4 | 8.4 | 1.3 |
| hin | broad | **4.4** | 0.7 | 6.4 | 1.0 | 6.3 | 1.0 |
| ind | broad | 37.9 | 5.3 | **34.9** | 5.3 | 39.3 | 6.1 |
| ind | narrow | 43.1 | 5.4 | **43.0** | 5.6 | 43.1 | 5.6 |
| jpn | narrow | **6.5** | 0.6 | 6.8 | 0.6 | 6.6 | 0.8 |
| kat | broad | **0.0** | 0.0 | **0.0** | 0.0 | 1.0 | 0.8 |
| kor | narrow | **23.4** | 4.1 | 25.3 | 4.4 | 25.8 | 4.6 |
| mya | broad | **35.1** | 6.5 | 36.0 | 6.9 | 88.0 | 17.4 |
| rus | narrow | **1.9** | 0.2 | 2.4 | 0.3 | 5.0 | 1.5 |
| spa ca | broad | **1.1** | 0.1 | 1.3 | 0.1 | 2.2 | 0.7 |
| spa ca | narrow | 2.3 | 0.3 | **2.2** | 0.3 | 2.8 | 0.6 |
| spa la | broad | **1.4** | 0.1 | 1.5 | 0.2 | 1.9 | 0.6 |
| spa la | narrow | **2.6** | 0.3 | 2.7 | 0.3 | 2.7 | 0.4 |
| tgl | broad | **28.4** | 4.6 | 31.2 | 5.2 | 33.9 | 5.0 |
| tgl | narrow | **45.5** | 6.4 | 47.3 | 7.0 | 48.6 | 6.9 |
| tha | broad | 12.5 | 2.6 | **11.1** | 2.5 | 12.1 | 3.1 |
| tur | broad | 50.6 | 7.8 | 52.3 | 7.5 | **49.1** | 7.2 |
| tur | narrow | 55.1 | 7.6 | 55.6 | 8.3 | **54.8** | 8.0 |
| vie | narrow | **1.5** | 0.8 | 1.6 | 0.8 | 2.6 | 1.5 |
| zul | broad | 65.9 | 10.7 | **9.8** | 0.9 | 91.4 | 12.0 |

## [Data](https://github.com/theDebbister/masterThesis/tree/master/data)
The data folder contains all the data I have worked with. I used two datasets:

* [WikiPron](https://github.com/CUNY-CL/wikipron)
* *The North Wind and the Sun* short stories

Both are explained in more detail in the [data](https://github.com/theDebbister/masterThesis/tree/master/data) folder. 

## Models

The model I used for my experiments is the [g2p-seq2seq](https://github.com/cmusphinx/g2p-seq2seq) model presented by CMUSphinx.
Everything concernign the models and the training is found in the [model](https://github.com/theDebbister/masterThesis/tree/master/models) folder.




