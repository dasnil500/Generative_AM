import streamlit as st
import re
import requests

API_URL = "https://api-inference.huggingface.co/models/dasnil500/end-to-end-am"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

# Load the pre-trained model and tokenizer
# checkpoint_path = "Frontend/"
# model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint_path)
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# model = model.to(device)
# tokenizer = AutoTokenizer.from_pretrained('t5-base', model_max_length=512)

# I do not understand the reason behind the protest. Farm law will greatly benefit small & marginal farmers of our country.Because, currently they cannot bargain for their produce and get a better price and cannot invest in technology to improve the productivity of the farms. This law will allow farmers to sell their product outside APMC “mandis” to whoever they want and get better price for their produce. We appreciate Government’s sensitivity towards us. But Government should listen our side too. This law will dismantle the minimum support price (MSP) system. Because, over time big corporate houses will dictate terms and we will end up getting less for our crops we produce. Government should give us a legal assurance that the MSP system will continue alongside.
def main():
    st.title("A Framework for Argument Mining")
    st.sidebar.title("Settings")
    # Text input from the user
    input_sentence = st.text_area("Enter your text:", height=200)
    st.sidebar.button("Fetch Top 10 Twitter Posts")
    st.sidebar.button("Fetch Top 300 Twitter using API")
    option = st.sidebar.selectbox("Select a topic:", ["Topic 1", "Topic 2", "Topic 3"])
    
    if st.button("Generate Output"):
        if input_sentence:
            # # Tokenize the input text
            # input_ids = tokenizer.encode(input_sentence, return_tensors="pt", max_length=512, truncation=True).to(device)

            # # Generate output using the model
            # output = model.generate(input_ids, max_length=512, num_return_sequences=1, num_beams=8)
            # generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
            output = query({
                "inputs": input_sentence,
                "parameters" : {"max_length": 512}
            })
            if (len(output) == 0):
                generated_text = ""
            else:
                generated_text = output[0]['generated_text']
            print(generated_text)


            if (len(generated_text) == 0):
                st.write(f"No arguments detected, please try with a bigger paragraph.")
            else:

                pattern = r'\[(.*?)\]'

                # Find all matches in the text
                matches = re.findall(pattern, generated_text, re.DOTALL)
                print(matches)
                # Initialize lists to store extracted data
                text1_list = []
                text2_list = []
                type_list = []
                relation_list = []
                text_type_rel = {"Claim":[],"Premise":[],"MajorClaim":[]}

                # Process each match
                for match in matches:
                    # parts = match.split('|')
                    parts = re.split(r'[|=]',match)
                    print(parts)
                    if(parts[1].strip()=="Claim"):
                        text_type_rel["Claim"].append(parts[0].strip())
                    if(parts[1].strip()=="Premise"):
                        text_type_rel["Premise"].append(parts[0].strip())
                    if(parts[1].strip()=="MajorClaim"):
                        text_type_rel["MajorClaim"].append(parts[0].strip())
                    print("\n\n")
                    print(text_type_rel)
                    if len(parts) == 4:
                        text1_list.append(parts[0].strip())
                        text2_list.append(parts[3].strip())
                        type_list.append(parts[1].strip())
                        relation_list.append(parts[2].strip())
                    if len(parts)==2:
                        text1_list.append(parts[0].strip())
                        text2_list.append('.')
                        type_list.append(parts[1].strip())
                        relation_list.append('.')
                output_text =''
                for i in range(len(text1_list)):
                    st.subheader(f"{i + 1}")
                    # output_text+="\n"
                    x_claim='Claim'
                    x_majorclaim='MajorClaim'
                    x_premise='Premise'
                    x=''
                    if(text2_list[i] in text_type_rel["Claim"]):
                        x=x_claim
                    if(text2_list[i] in text_type_rel["Premise"]):
                        x=x_premise
                    if(text2_list[i] in text_type_rel["MajorClaim"]):
                        x=x_majorclaim
                    if(type_list[i]!='Claim'):
                        st.write(f"{type_list[i]} : {text1_list[i]}")
                        st.write(f"{x}: {text2_list[i]}")
                        st.write(f"Relation: {relation_list[i]}")
                    else:
                        st.write(f"{type_list[i]} : {text1_list[i]}")

                


            # Display the generated text
            # st.subheader("Argumented Mining Data:")
            # st.write(output_text)
        else:
            st.warning("Please enter some text.")

if __name__ == "__main__":
    main()
