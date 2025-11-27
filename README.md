# AI-pet-agent
An AI agent to help prospective pet owners with their pet adoption search.

## Background

### Old Problem statement

The original problem that I proposed was to create an AI agent for pet owners such that they could ask any type of pet related questions such as “How much should I feed my dog?”, “What pet food is best for my kitten?”, “Are grapes poisonous to my cat?”, etc. However, I quickly found that this was quite a broad and ambitious goal. The main problem I ran into was the information base as there was no centralized api or dataset that could contain all information on cats, dogs, and other pets.
	Even though I could gather my own corpus of information from websites such as petMD, it would still be incomplete as you could not get all possible information on pets, especially in the short amount of time that was allotted to this project. I wanted to prioritize accuracy and robustness over scope thus I sought to reduce the scope of my project. Of course, it could still be possible to make a small demo and constrict the scope to a more specific category of questions that way the information could be more robust and the agent could produce more accurate information, but I thought it may be better to just pivot altogether and try a new problem with more structured data and information.

### New Problem statement
#### What is the problem?
The new problem is creating an AI agent for prospective pet owners and easing the process of finding an available pet up for adoption that matches the person’s preferences. The goal is to allow people to prompt the agent with a query like “I want a young white cat who has a bubbly personality and loves to cuddle near Boston.” and the agent will return a list of relevant adoptable pets along with a short description and a link to their information. This problem is a better problem to tackle because it has a smaller scope of information and more structured data that can be accessed and processed.
	This AI agent tackles the problem of finding the right pet to adopt. It is often very overwhelming when scrolling the internet for potential pets to add to your life. It is a big commitment and finding the right pet is an important step in the process to ensure the happiness and well-being of both the adopter and pet. Thus, it is important to have a place where someone could ask questions and find relevant pets and suggestions based on their preferences to help guide their search during this big and exciting moment.

#### Why is this problem interesting?
This problem is an interesting problem to tackle because it is applicable to a wide range of people and it helps support a good cause. Additionally, this problem is interesting and relevant to me as a volunteer at a local Boston animal shelter that often gets a lot of different animals coming in. It is always helpful to have a tool to allow people to find the perfect pet for them and give them background information and guidance into finding which pet is perfect for them. 
On the more technical side, this problem is interesting to see how I can implement such an AI agent, what search algorithms work best, and seeing how well an agent can provide accuate and reliable information. It will be exciting to learn the different models that can be used and how a language model will interact with different types of adoption data.

#### What is the proposed approach?
The approach is for the user to input a query, then the model will parse the query, obtain the relevent attribute information and descriptions, filter out animals that are most relevant then retrive the most relevant animals from the database using a search method such as TF-IDF to rank the animal's description to the user's query. I used prompting formats to guide the language model to generate repsonses and call the search methods that I defined and used a pretrained language model from hugging face. 

#### What is the ratinoal behind the approach?
I used this approach because it seemed like the best approach to create an AI adoption pet agent. First, Parsing the query to only obtain the relevant attribute information and description ensures that only the most important information is processed thus reducing noise and allowing for more accurate retrival and ranking. Additionally, filtering is used to ensure that only relevant animals are returned, this way, even if a description may match a user's query more, the agent prioritizes the basic attributes such as species, age, and location that are more practical and relevant to adopting pets. Finally, TF-IDF was a good search method to use because it is simple, fast, and an intuitive method for ranking relevance.

## Methodologies

### Overall pipeline

### Algorithms and methods

### Assumptions and design choices

### Limitations

## Experiement setup

### Data

#### Toy Corpus
In this project I used a toy corpus of about 50 pets which serves as a placeholder as I wait for my Rescue Group Adoptable Pets API key request to be processed. The toy corpus was generated by ChatGPT from an example entry that I provided. This was done to allow for a diverse and robust corpus of data that was not feasible for me to write by myself. The generated toy corpus has a divsere range of animals that have a range of species types, location, and description.

![Species Distribution](https://github.com/rayna-yu/AI-pet-agent/figures/data/species.png)

I modeled the example data entries as closely as I could to existing example data on the internet and my request for the key is currently being processed.

#### Rescue Group API
I determined that Rescue Group was the best API to use because it provided me the servies that was necessary for my AI agent. It is a non profit group that provides an adoptable pet data api that has been in use since 2006. It is updated and expanded on a regular basis and has no limitations on total requests, records per requests, or the number of results. It is designed for live queries and allows users to search for animals using a combination of fileds such as postal code, distance, size, age, breed, etc. 

### Implementation

#### Models 

#### Parameters

#### Computing enviroment

## Results

## Discussion

### Comparision to existing approaches

### Further work and improvements

## Conclusion

## References

## Run the code
