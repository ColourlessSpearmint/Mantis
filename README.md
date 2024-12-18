# Mantis

This project is a digital emulator and neural network agent for the card game [Mantis](https://www.explodingkittens.com/products/mantis).

## Planned Features/Roadmap

### Stuff I know how to do

- &#10004; **Project Structure**: The roadmap and file structure of the project.
- &#10006; **Mantis Logic**: A digital emulator for Mantis, taking input from each player and updating the game state based on the the [official rules](https://cdn.shopify.com/s/files/1/0345/9180/1483/files/Copy_of_Mantis_Instructions_18NOV21.pdf?v=1709370758).
- &#10006; **Playable Notebook**: An implementation of game logic that queries each player for their input and renders a CLI user interface based  on the game state.
- &#10006; **Scripted Bots**: Algorithmic bots that employ a simple prebuilt strategy and act as players.
- &#10006; **Bot Integration**: Integrate scripted bots into playable notebook.
- &#10004; **Plan Neural Network Architecture**: Inputs, hidden layers, and outputs of the neural network.

### Stuff I need to figure out (expect frequent changes as I become less ignorant)

- &#10006; **Tests**: Tests to verify game mechanic implementation is functional.
- &#10006; **Implement Neural Network Architecture**: Something in PyTorch; I dunno.
- &#10006; **Training Method**: PyTorch implementation of [Reinforcement Q-learning](https://en.wikipedia.org/wiki/Q-learning).
- &#10006; **Training Environment**: Loss function, optimizer, evaluation Metrics, etc.
- &#10006; **Train Model**: Probably a few hours of training time on my NVIDIA GTX 1650
- &#10006; **Integrate Model into Notebook**: Integrate trained model to playable notebook

## Network Architecture

### Input Layer: 

(7 x 4) + (1 x 4) + 3 = 35

- 7 nodes per player for the count of each color.
- 1 node per player for the number of cards in their Score Pile.
- 3 nodes for the potential colors of the card on the Draw Pile.

### Hidden Layers: 

64 x 2 = 128

- 64 neurons per layer; 2 layers

### Output Layer: 

1 x 4 = 4

- 1 node per player

## Usage

### Play

[![Open in Colab](https://img.shields.io/badge/Open%20in-Colab-blue?logo=google-colab)](https://colab.research.google.com/github/ColourlessSpearmint/Mantis/blob/main/notebooks/play_mantis.ipynb)

If you just want to play Mantis (against one of my bots or playing with friends), the `play_mantis.ipynb` Jupyter notebook is the easiest option. There's a Colab badge above, or you could clone the repo and run it locally.

```bash
git clone https://github.com/ColourlessSpearmint/Mantis.git
cd Mantis
pip install -r requirements.txt
jupyter notebook notebooks\play_mantis.ipynb
```

### Train

As of the time of writing, I haven't implemented training yet. I'll update this section when I do.

## Author

Developed by **Ethan Marks** ([@ColourlessSpearmint](https://github.com/ColourlessSpearmint)).

README artwork and original game design by the **Exploding Kittens Team** ([Official Website](https://www.explodingkittens.com/pages/about-exploding-kittens)).


## Incompetence

I've never done anything like this before, so I can guarentee that I will mess up frequently. I'm doing my best to employ future-proof practices, but earlier commits will probably be a bit of a mess. I'll try and develop on `feature/` and `development` branches, only pushing stable releases to `main`, but I will probably commit to the wrong branch at some point. Sorry in advance.

## License

This project is licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0).

## Credits

Images used in this project are sourced from the official [Mantis website](https://www.explodingkittens.com/products/mantis) and are used for decorative purposes only.
