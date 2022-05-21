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

There are no results available just yet. The thesis is still in progess. I will push results as soon as the thesis is completed.

## [Data](https://github.com/theDebbister/masterThesis/tree/master/data)
The data folder contains all the data I have worked with. I used two datasets:

* [WikiPron](https://github.com/CUNY-CL/wikipron)
* *The North Wind and the Sun* short stories

Both are explained in more detail in the [data](https://github.com/theDebbister/masterThesis/tree/master/data) folder. 

## Models

The model I used for my experiments is the [g2p-seq2seq](https://github.com/cmusphinx/g2p-seq2seq) model presented by CMUSphinx.
Everything concernign the models and the training is found in the [model](https://github.com/theDebbister/masterThesis/tree/master/models) folder.




