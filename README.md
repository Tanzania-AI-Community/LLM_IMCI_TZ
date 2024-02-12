# LLM_IMCI_TZ
Repository for Improving the Use of Integrated Management of Childhood Illness Protocols in Tanzania using LLMs

As part of the Global Grand Challenges _"Catalyzing Equitable Artificial Intelligence (AI) Use"_

**Improving the Use of Integrated Management of Childhood Illness Protocols in Tanzania**

Essa Mohamedali and Kalebu Gwalugano of the Tanzania AI Community in Tanzania will use ChatGPT-4 to develop a chatbot and support tool to help healthcare workers adhere to the Integrated Management of Child Illness (IMCI) guidelines and access updates and alternative treatment options by linking them to the latest research via their mobile phones. Access to formal training on the IMCI guidelines is limited for healthcare workers, particularly in the private sector, and its duration makes it prohibitively expensive for companies. They will convert the existing guidelines and algorithms into a chatbot version and use the GPT-4 framework to connect to the latest research. They will engage healthcare workers during the development stage and then implement and field test the support tool at three private health facilities in rural, urban, and peri-urban areas of Tanzania, to assess its usability.

https://gcgh.grandchallenges.org/grant/improving-use-integrated-management-childhood-illness-protocols-tanzania


## How to edit the docs?

### Installation

```
$ yarn
```

### Local Development

```
$ yarn start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

### Build

```
$ yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

### Deployment

Using SSH:

```
$ USE_SSH=true yarn deploy
```

Not using SSH:

```
$ GIT_USER=<Your GitHub username> yarn deploy
```

If you are using GitHub pages for hosting, this command is a convenient way to build the website and push to the `gh-pages` branch.
