
# Introduction

Conseil is a small telegram chatbot which takes in User voice messages and transcribes them. Currently, we only support generating TODOs from these transcripts but there are plans to have future workflows such as

- [ ] Support for generating general trends on user sentiments and thoughts (Eg. What you're feeling and the negative/positive trends )

- [ ] GPT-4V integration to help users log their daily meals OR to get labelled screenshots (KIV Not sure)

- [ ] Support for no more buttons -> We can just directly query the bot and it will be able to do what needs

# Running the Project

The project itself works off a single Modal endpoint which does everything that interfaces with a Cloudflare D1 Database that is only accesible using workers.

Therefore, in order to run this project locally, you'll need to do the following

1. Set up the Cloudflare D1 integration. To do so, navigate to the `cloudflare` folder, run `npm install` and then `npm run dev`. 

You should be prompted to set up your cloudflare account at some point, after which everything should work nicely

2. Sign up for a Modal account - The backend codes lives entirely on Modal and that's where all the `.envs` live. We have a total of 4 different name spaces

- `telebot` -> `TOKEN` which is your telegram bot
- `openai` -> `OPENAI_API_KEY` which is your OpenAI Api Key
- `cloudflare-ai` -> `ACCOUNT_ID` which is your cloudflare Account ID and `API_TOKEN` which is your Cloudflare API Token
- `cloudflare-db` -> `DB_URL` which is your cloudflare DB endpoint

3. Install all of the dependencies using `pip3 install -r requirements.txt`

4. Run the server on `modal serve modal/bot.py`

The endpoint here is deployed on Modal and our CI/CD automatically handles the deployment with every new push to `main`. We also have a small test suite using `pytest` which runs on CI.
