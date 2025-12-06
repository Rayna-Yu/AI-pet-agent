# AI-pet-agent
An AI agent to help prospective pet owners with their pet adoption search.

## Abstract

My project introduces an AI-powered agent designed to support prospective pet owners in finding adoptable animals that best align with their preferences. Users can use natural-language queries such as "I want a playful lap cat who is on the younger side and is near Boston" and the agent will return a list of relevant pets with information on their attributes and description. The agent interprets the user's intent by extracting the key attributues such as species, age, personality, and location, filters for the relevant species and applies TF-IDF based retrieval to rank descriptions by simmilarity to the query. A toy corpus of 50 divserse animals was used while developing while waiting to gain access ot the Rescue Group Adoptable Pets API. Initial experimentation shows that the agent can accurately atch user preferences and provide meaningful recommendations.

## Background

### Old Problem statement

The original problem that I proposed was to create an AI agent for pet owners such that they could ask any type of pet related questions such as “How much should I feed my dog?”, “What pet food is best for my kitten?”, “Are grapes poisonous to my cat?”, etc. However, I quickly found that this was quite a broad and ambitious goal. The main problem I ran into was the information base as there was no centralized api or dataset that could contain all information on cats, dogs, and other pets.

Even though I could gather my own corpus of information from websites such as petMD, it would still be incomplete as you could not get all possible information on pets. I wanted to prioritize accuracy and robustness over scope thus I sought to reduce the scope of my project. Of course, it could still be possible to make a small demo and constrict the scope to a more specific category of questions that way the information could be more robust and the agent could produce more accurate information, but I thought it may be better to just pivot altogether and try a new problem with more structured data and information.

### New Problem statement
#### What is the problem?
The new problem is creating an AI agent for prospective pet owners and easing the process of finding an available pet up for adoption that matches the user’s preferences. The goal is to allow people to prompt the agent with a query like “I want a young white cat who has a bubbly personality and loves to cuddle near Boston.” and the agent will return a list of relevant adoptable pets along with a short description and a link to their information (if provided). This problem is a better problem to tackle because it has a smaller scope of information and more structured data that can be accessed and processed.

This AI agent tackles the problem of finding the right pet to adopt. It is often very overwhelming when scrolling the internet for potential pets to add to your life. It is a big commitment and finding the right pet is an important step in the process to ensure the happiness and well-being of both the adopter and pet. Thus, it is important to have a place where someone could ask questions and find relevant pets and suggestions based on their preferences to help guide their search during this big and exciting moment.

#### Why is this problem interesting?
This problem is an interesting problem to tackle because it is applicable to a wide range of people and it helps support a good cause. Additionally, this problem is interesting and relevant to me as a volunteer at a local Boston animal shelter that often gets a lot of different animals coming in. It is always helpful to have a tool to allow people to find the perfect pet for them and give them background information and guidance into finding which pet is perfect for them. 

On the more technical side, this problem is interesting to see how I can implement such an AI agent, what search algorithms work best, and seeing how well an agent can provide accuate and reliable information. It will be exciting to learn the different models that can be used and how a language model will interact with different types of adoption data.

#### What is the proposed approach?
The approach is for the user to input a query, then the model will parse the query, obtain the relevent attribute information and descriptions, filter out animals that are most relevant then retrive the most relevant animals from the database using a search method such as TF-IDF to rank the animal's description to the user's query. I used prompting formats to guide the language model to generate repsonses and call the search methods that I defined and used a pretrained language model from hugging face. 

#### What is the ratinoal behind the approach?
I used this approach because it seemed like the best approach to create an AI adoption pet agent. First, Parsing the query to only obtain the relevant attribute information and description ensures that only the most important information is processed thus reducing noise and allowing for more accurate retrival and ranking. Additionally, filtering is used to ensure that only relevant species are returned, this way, even if a description may match a user's query more, the agent prioritizes the species which is the most relevent attribute to consider when adopting a pet. Finally, TF-IDF was a good search method to use because it is simple, fast, and an intuitive method for ranking relevance.

## Methodologies

### Overall pipeline
1. Data normalization: Each row pet entry in the toy corpus is converted into a strcutured disctionary containing the attributes like name, species, breed, age, sex, description, and location and a text field that is used for retrieval.
2. Test preprocessing and tokenization: text from each animal, title and attribute text blob, is lowercased and tokenized using a regex tokenizer.
3. TF-IDF vetorization: Term frequency is computed per document (text blob per animal) and document frequency and IDF values are computed globally for the toy corpus
4. Cosine-simalrity search: The cosine similarity between the query vector and each animal in the corpus's vector are then computed and ranked to return the top-k candidates.
5. ReAct agent reasoning loop: The user query is passed to a small intruction-tuned LLM (Qwen2.5-0.5B-Instrcut) and the agent interprets the query, decides whether to use the search tool or finish, receives observations from the search toops, and iteratively refines the reasoning for up to max_steps.
6. Final answer: Once the LLM produces "finish[answer='...']", the agent returns the final reasoning trace and the model's generated recommendations.
   
### Assumptions and design choices
My current implementation is heavily dependent on getting personality information from the description. Thus, one assumption made is that the descriptions contain enough information to meaningfully correlated with the user intent. Of course, the search still works without the description, but it is not as robust. Additionally, it is currently assumed that the user querires will be relevent to pet adoption. Thus I take for granted that there will be information in the query about species, age, location, and other behavioral traits. Furthermore, as of now, because I am using a toy corpus, the data is ensured to be very consistent, thus the normalization step assums each JSON entry follows a consistent structure which is not true for real data. Finally, I assumed that a small model is sufficient in capability to parse user intent and produce reliable tool calls.

### Limitations
As of now, I am limited to the toy corpus which is relatively small and lacks the diversity of real-world adoption data. It is also too perfect and consistent in structure which does not reflect any practical datasets or APIs that could be integrated. Additionally, TF-IDF can not capture semantic similarity or synonyms like "cuddly" and "affectionate". An additional limitation is the limitation in the model that we used form hugging face. Qwen2.5-0.5B-Instrcut is a small model and thus it has constraints in accuracy and may misinterpret queries or fail to produce ideal reasoning steps.

### Experiement setup

#### Toy Corpus
In this project I used a toy corpus of about 50 pets which serves as a placeholder as I wait for my Rescue Group Adoptable Pets API key request to be processed. The toy corpus was generated by ChatGPT from an example entry that I provided. This was done to allow for a diverse and robust corpus of data that was not feasible for me to write by myself. The generated toy corpus has a divsere range of animals that have a range of species types, location, and description.

![Summary of animal information](https://github.com/Rayna-Yu/AI-pet-agent/blob/main/figures/data/summary.png)

![Species Distribution](https://github.com/Rayna-Yu/AI-pet-agent/blob/main/figures/data/species.png)

![Age Distribution](https://github.com/Rayna-Yu/AI-pet-agent/blob/main/figures/data/age.png)

I modeled the example data entries as closely as I could to existing example data on the internet and my request for the key is currently being processed.

#### Rescue Group API
Eventhough I could not incooperate it into my project at this time, I determined that Rescue Group was the best API to use because it provided me the servies that was necessary for my AI agent. It is a non profit group that provides an adoptable pet data api that has been in use since 2006. It is updated and expanded on a regular basis and has no limitations on total requests, records per requests, or the number of results. It is designed for live queries and allows users to search for animals using a combination of fileds such as postal code, distance, size, age, breed, etc.

#### Hardware
I used google colab which provides access to a GPU.

#### Model configuration
Model: Qwen2.5-0.5B-Instrcut

Decoding: temperature=0.1, do_sample=True

Max tokens: 300

I used a temperature of 0.1, because lower temperatures means reduced randomness in the model's output. This makes the generation of recommendations more deterministic and focused.

I used a do_sample because it prevents the model from defaulting to purely greedy decoding. This allows the model to consider multiple likely tokens while still remaining controlled. This can yield slightly more natural responses more similar to talking with a real agent.

I used max tokens because it was a reasonable upper boudn that ensured the model had enough space to produce actual coherent and accurate responses without cuttin off the inputs. I found while playing around with the model that a max token of 150 sometimes caused the model to cut itself off, thus I increased it to 300. This makes sure that the generation is efficient while preventing overly long or irrelevent text.

#### Evaluation Metrics
Results where judged qualitatively by how well it was able to respect the species/age/locations, whether the descriptions match and how well they matched, and whether the agent followed the formatting that I specified. Additionally, I evaluated the agent on how well it was able to use the tools to filter for the specific species. For example, if a user wants a cat, the agent only returns cats.

## Results

The results of the trial runs that I ran were very promising. My first trial I prompted the agent with "I want a young, cuddly calico cat in Boston." This was the most basic query that I could provide it with simple and clear information about age, species, location, and a descriptor on personality. This query was also provided in the preamble as an example to the LLM.

The resulting asnwer was: "Based on your preferences, I found the following pets: 1. Luna, a young, cuddly Calico cat in Boston. 2. Ruby, a Calico Exotic Shorthair cat in Providence, RI. 3. Jack, a Border Collie dog in Boston." 

This was my first trial, thus I did not implement any filtering yet which explains why a dog was returned even though the query asks for a cat. Aside from that mistake, it seems like the agent was able to return accurate and reasonable results. The first pet was an exact match to the query: a young, cuddly, calico cat in boston. The second pet is a cat and a very close match in description ("Cuddly and calm, enjoys lounging in sunny spots."), matching cuddly exactly, and location, but not a match in age or breed. The third pet however, was a bad response because the agent returned a dog when I explicitly asked for a cat.

After adding some filtering for species and additional formatting guides for the output I asked it the same question and got the answer: 

Next, I prompted it with a query not provided in the preamble and got the result: "I have found 3 cats that match your description: 1. Luna — Young, Calico in Boston, MA. 2. Ruby — Adult, Exotic Shorthair in Providence, RI. 3. Maggie — Young, Manx in Albany, NY."

This showed a much better improvement from the previous search as with the filtering and the new preamble the llm was able to only return pets that match the species.

Next I tested the llm out on an example query for dogs. 

And I got a response of: The user has found 5 adult, playful dogs in Boston: 1. Rocky, 2. Jack, 3. Riley, 4. Buster, 5. Moose.

As can be seen, the agent was able to produce a result, but it did not adhere to the formatting rules that I specified in the preamble. Instead it just listed the names with no description or other information. Eventhough it did not follow the formatting rules I put in, it was able to properly use the search method and all the animals returned were the right species and relevant to the query. As seen by the action: 

Action: search[query="adult playful dog Boston", species="dog", k=5]
{"tool": "search", "query": "adult playful dog Boston", "results": [{"id": "2006", "name": "Rocky", "species": "Dog", "breed": "Pit Bull Terrier", "age": "Adult", "sex": "Male", "location": "Boston, MA", "score": 0.28732645343031166, "snippet": "Energetic and loyal; loves toys and needs an active home."}, {"id": "2039", "name": "Jack", "species": "Dog", "breed": "Border Collie", "age": "Young", "sex": "Female", "location": "Boston, MA", "score": 0.264071593732683, "snippet": "Smart and energetic; loves to run and learn tricks."}, {"id": "2024", "name": "Riley", "species": "Dog", "breed": "Australian Shepherd", "age": "Young", "sex": "Male", "location": "Boston, MA", "score": 0.2522828621314104, "snippet": "Very smart and active, loves games and mental challenges."}, {"id": "2022", "name": "Buster", "species": "Dog", "breed": "Dalmatian", "age": "Adult", "sex": "Male", "location": "Syracuse, NY", "score": 0.18809188505815283, "snippet": "Loves to run, very energetic and playful."}, {"id": "2035", "name": "Moose", "species": "Dog", "breed": "Saint Bernard", "age": "Adult", "sex": "Female", "location": "Buffalo, NY", "score": 0.17636455964081585, "snippet": "Gentle giant; calm and loves children."}

After further refining the output rules in the preamble I was able to obtain an answer of: I have found 2 dogs that match your description: 1. Rocky — Adult, Pit Bull Terrier in Boston, MA. 2. Jack — Young, Border Collie in Boston, MA. 

Once the agent was able to produce satisfactory answers to the example prompt I provided it, I additionally prompted the agent with more complex and query such as "I'm thinking of getting a cat that will like to go on long walks with me but also cuddle with me and watch TV." 

The resulting answer was: Bella — Senior, Maine Coon in Somerville, MA. Bella is a gentle senior cat who loves brushing and quiet spaces. She is also a cuddly cat that enjoys watching TV.

The result was a decent match to the query and got the cuddly part correct. However, I did notice it hallucinated some attributes to match the query when that information did not appear in the actual data. For example the output says that Bella enjoys watching TV, but this is not mentioned at all in her description: 

"id": "2003",
      "type": "animals",
      "attributes": {
        "animalName": "Bella",
        "animalSpecies": "Cat",
        "animalBreed": "Maine Coon",
        "animalAgeString": "Senior",
        "animalSex": "Female",
        "animalDescriptionPlain": "Gentle senior cat who loves brushing and quiet spaces.",
        "animalLocation": "Somerville, MA",
        "animalPictures": [
            { "urlSecureFullsize": "https://example.com/bella.jpg" }
        ]

This continued to be a persistent issue when testing out the agent that I hope to address in the future.

Additionally, the key attributes were not always extracted. For example when asking for a playful young dog in Boston the action would be: Action: search[query="young dog Boston", species="dog", k=3] instead of Action: search[query="playful young dog Boston", species="dog", k=3]. This is evidence that I will need to further refine the way the agent processes the query to extract the relevent key words and attributes. However, even though it is not perfect in finding relevent attributes, it still is able to return decent results.

Finally, I also notices that as the queries become more complex the agent started adding random parameters to the search method that do not exist and I did not specify. More specifically, the agent often added the parameter of location which caused errors thus making the agent loop until the max steps are reached and return no final answer. 

## Further work and improvements
As can be seen in the results, the agent is far from perfect and has a long way to go to become a useful tool. It messes up a lot and does not always adhere to the rules and tools that I set for it. I hope to further improve the agent by better prompt engineering the llm to produce higher quality and more consistent results and adding guard rails to prevent the agent from adding parameters to the search method.

I also hope to improve this project by connecting the agent to the real Rescue Group Adoptable Pets API rather than using the toy corpus. I also hope, once I get access to the API, I can display images or links that are connected to the pets so that users can go directly to adoption pages and see if the suggested pets are right for them to adopt them. 

Additionally, I want to refine the filtering and search methods to be more specific to pet information. For filtering, right now my search method only supports filtering by species. However, I want to also add filtering by location and other attributes, but this proved to be too finicky to confidently implement in the given amount of time. For searching, as of now the TF-IDF and cosine simalrity are more tailored to documents of information like wikipedia and thus are more suited for tasks such as Question and Answering. I hope to refine these methods and research more relevant algorithms that pretain to the task that this agent is performing. TF-IDF is very sensitive to noisy and short descriptions which is not ideal when applied to pet adoption information as they are usually very short descriptions. Additionally, as mentioned before it fails at semantic simlarities and can only perform token overlap, thus it would greatly improve the agent to find a more relevant search method. 

Further improvements can be made to efficiency. The agent takes a long time to produce an answer, thus, I hope to speed up the process and further enhance the algorithms and methodologies to improve the time it takes to produce answers to user queries. 

Finally, as of now, the command line interactions are very impractical and not ideal. A future enhancement would be to add a user interface to allow people to interact with the agent in a more practical and convinenet way.

## Conclusion
This project is an AI agent designed to assist prospective pet adopters by matching their preferences with available adoptable pets. Through natural-language query parsing, filtering, and TF-IDF-based retrieval, the agent can provide personalized recommendations to the user. Initial results are promising, but there are clear opportunities for improvement, including integrating real-world adoption data, refining search and filtering methods, and enhancing response consistency. Overall, this agent demonstrates the potential of combining AI and information retrieval to simplify and personalize the pet adoption process.

## References
Code template: https://github.com/VirtuosoResearch/CS4100_project 

Rescue Group API: https://rescuegroups.org/services/adoptable-pet-data-api/

## Run the code

To run the code you can use the provided jupiter notebook. If you want, you can play around with the prompt in the last cell to test out the agent and see what it responds. 
