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
    
    generated_text = None  # Initialize generated_text variable

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
            print(f"Model output is :\n{output}\n")

            try:
                generated_text = output[0]['generated_text']
            except KeyError:
                st.write("Please wait for 40 seconds to start the engine....")

        else:
            st.warning("Please enter some argumentative text....")

    # Rest of your code
    if generated_text:
        # ------------------------------------------------------------------
        # Define a regular expression pattern to match [ text ] patterns
        pattern = r'\[([^]]+)\]'

        # Find all matches in the text
        sentences = re.findall(pattern, generated_text)
        if not sentences:
            st.write ("No arguments detected... Please try with any argumentative paragraphs...")
        # print (sentences)

        # Define a regular expression pattern to match Claims, MajorClaims, or Premises
        pattern1 = r'\s*(.+?)\s+\|\s+(Claim|MajorClaim|Premise)\s*$'

        gt_argument_types = ["Premise", "Claim", "MajorClaim"]
        list1 = list()

        for pattern_string in sentences:
            match = re.match(pattern1, pattern_string)
            # print (match)
            if match:
                argument = match.group(1)
                argument = ",".join(argument.split(" ,")).strip()
                arg_type = match.group(2)
                if arg_type in gt_argument_types:
                    list1.append((arg_type,argument))
        # print (list1)


        # ------------------------------------------------------------------
        final_list_of_tuples = list()
        pattern2 = r'(.+?)\s+\|\s+(Claim|MajorClaim|Premise)(?:\s+\|\s+(Support|Attack)\s*=\s*(.*?))?$'

        for pattern_string in sentences:
            match = re.match(pattern2, pattern_string)

            if match:
                argument = match.group(1)
                argument = ",".join(argument.split(" ,")).strip()
                arg_type = match.group(2)
                relation = match.group(3)
                connected_to = match.group(4)
                connected_to = ",".join(connected_to.split(" ,")).strip()

                for item in list1:
                    if (item[1]) == connected_to:
                        final_list_of_tuples.append((item, argument, arg_type, relation))

        # print (list1)
        # print (final_list_of_tuples)


        # ------------------------------------------------------------------
        if (final_list_of_tuples):

            # Create a dictionary to group the data
            grouped_data = {}

            for item in final_list_of_tuples:
                argument_tuple = item[0]  # The first element in the tuple is the claim
                source_argument = item[1]  # The second element in the tuple is the premise
                source_type = item[2]  # The third element in the tuple is the relation type
                relation = item[3]  # The fourth element in the tuple is the relation

                # Check if the claim is already in the grouped data
                if argument_tuple in grouped_data:
                    # Append the premise and relation to the existing claim
                    grouped_data[argument_tuple].append((source_argument, source_type, relation))
                else:
                    # Create a new entry for the claim and initialize it with the premise and relation
                    grouped_data[argument_tuple] = [(source_argument, source_type, relation)]

            # print (grouped_data)

            # Print the grouped data
            for tgt, src in grouped_data.items():
                st.markdown(f"<b style='font-size:{'25px'}'>{tgt[0]}</b><br>{tgt[1]}", unsafe_allow_html=True)
                for item in src:
                    src_comp, src_type, relation = item
                    st.markdown(f"<b style='font-size:{'20px'}'>{src_type}:  </b>{src_comp}", unsafe_allow_html=True)
                    st.markdown(f"<b style='font-size:{'20px'}'>Relation:  </b>{relation}", unsafe_allow_html=True)

        # else block means there are no claim-premise pairs are detected
        else:
            for tgt in list1:
                st.markdown(f"<b style='font-size:{'25px'}'>{tgt[0]}</b><br>{tgt[1]}\n", unsafe_allow_html=True)


        # --------------------------------------------------------------------------------
        # pairs are detected but claim or majorclaim are not detected
        if (len(final_list_of_tuples) == 0 and len(list1) == 0):
            st.markdown(f"<b style='font-size:{'25px'}'>Note:  </b>Listing down argument pairs with low confidence....", unsafe_allow_html=True)
            for pattern_string in sentences:
                match = re.match(pattern2, pattern_string)
                if match:
                    argument = match.group(1)
                    argument = ",".join(argument.split(" ,")).strip()
                    arg_type = match.group(2)
                    relation = match.group(3)
                    connected_to = match.group(4)
                    connected_to = ",".join(connected_to.split(" ,")).strip()
                    st.markdown(f"<b style='font-size:{'25px'}'>Premise/Claim</b><br>{connected_to}", unsafe_allow_html=True)
                    st.markdown(f"<b style='font-size:{'20px'}'>{arg_type}:  </b>{argument}", unsafe_allow_html=True)
                    st.markdown(f"<b style='font-size:{'20px'}'>Relation:  </b>{relation}", unsafe_allow_html=True)
                    

if __name__ == "__main__":
    main()
