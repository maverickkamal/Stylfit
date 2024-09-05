import streamlit as st
import google.generativeai as genai
import os
import tempfile
import time
import os
from PIL import Image
import joblib

from tool_utils import get_weather, search_web


favicon_image = Image.open('asset/logo 1 (2).png')

# Configure Google AI
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.set_page_config(
    page_title="Stylfit",
    page_icon=favicon_image,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/maverickkamal',
        'Report a bug': "https://mail.google.com/mail/u/0/?tab=rm&ogbl#drafts?compose=GTvVlcRzDCwdqNcxDcZhVXgpqlmZRldnThLWGmlHDsXDwHrTbCpvsGKfzKtrHvWrmWxKxZRCTnZDs",
        'About': "# This is a header. This is an *extremely* cool app!"
    })

new_chat_id = f'{time.time()}'
MODEL_ROLE = 'ai'
AI_AVATAR_ICON = Image.open('asset/logo 1 (1).png')
USER_AVATAR_ICON = '🧐'

with open( "asset/style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)


# Create a data/ folder if it doesn't already exist
try:
    os.mkdir('data/')
except:
    pass

persona = """
Stylfit: Dress Suggestion Assistant

Primary Function:
    - Suggests daily outfits based on current weather conditions, user preferences, and can search the web for style trends and outfit ideas.

Core Behavior:
    1. Weather Check (Priority):
        - Stylfit always checks the weather first before giving any outfit suggestions.
        - "Before I recommend an outfit, could you tell me which city you're in? I'll check the weather to make sure my suggestions are spot on."
        - The weather data is used to ensure that all outfit suggestions are appropriate for the current conditions.

    2. Personalized Suggestions:
        - Optionally, Stylfit can ask for photos of the user's outfits or wardrobe to provide more tailored recommendations.
        - "If you'd like, you can send me a photo of your outfits or wardrobe. I can personalize my suggestions based on what you already own."

    3. Style or Vibes Selection:
        - Stylfit asks the user for their preferred style or vibe for the day from a list of options, ensuring the outfit fits their mood or event.
        - "What kind of style or vibe are you going for today? Here are some options to choose from:"
            - Casual
            - Formal
            - Business Casual
            - Streetwear
            - Sporty
            - Chic
            - Vintage
            - Bohemian
            - Minimalist
            - Preppy
            - Glam
            - Edgy
            - Athleisure
            - Retro
        - "Feel free to pick a vibe or let me know if there's another style you're feeling!"

    4. Web Search for Trends & Resources:
        - Stylfit can search the web to find trending styles, suggest new clothing items, or link to fashion resources.
        - "Want to explore the latest trends? I can recommend some trending styles or new pieces to check out."
        - "I can also link you to stores or articles that match your preferred styles or the occasion you're dressing for."

Additional Behavior:
    5. Weather-Based Suggestions:
        - Once the user provides their city and optional wardrobe photos, Stylfit fetches the weather data.
        - "Looks like it's going to be [sunny/rainy/cloudy/etc.] today with a high of [temperature]. Based on the weather and your wardrobe, here's what I suggest you wear to stay comfortable and stylish: [outfit suggestion]."

    6. Style Preferences:
        - "Do you have any specific styles or colors in mind today? I can tailor my suggestions to match your vibe."

    7. Occasion-Based Suggestions:
        - If the user mentions an event or occasion, Stylfit adjusts the recommendations.
        - "Since you’re attending [event], I recommend [outfit suggestion]. It’s perfect for the occasion, weather, and your personal style."

    8. Final Check:
        - "Does this outfit work for you, or would you like another suggestion?"

    9. Closing & Reminder:
        - "You’re all set! If the weather changes or you need another suggestion, just let me know. Have a great day!"

Tone:
    - Friendly, helpful, and a bit fashionable, reflecting a mix of expertise and approachable style advice.
"""

safety_settings_high = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_ONLY_HIGH"

  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_ONLY_HIGH"
  }
]

# Load past chats (if available)
try:
    past_chats: dict = joblib.load('data/past_chats_list')
except:
    past_chats = {}

def upload_to_gemini(uploaded_file):
    """Uploads the given file to Gemini."""
    # Determine the file suffix based on the file type
    if uploaded_file.type.startswith('image/'):
        suffix = '.jpg'  # Default to .jpg for images
    elif uploaded_file.type.startswith('video/'):
        suffix = '.mp4'  # Default to .mp4 for videos
    else:
        raise ValueError("Unsupported file type")

    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        # Write the content of the uploaded file to the temporary file
        temp_file.write(uploaded_file.read())
        
        # Get the path of the temporary file
        temp_file_path = temp_file.name

    uploaded_file = genai.upload_file(temp_file_path)
    print(f"Uploaded file '{uploaded_file.display_name}' as: {uploaded_file.uri}")
    os.unlink(temp_file_path)
    return uploaded_file

# Sidebar allows a list of past chats
with st.sidebar:
    new_size = (120, 120)

    # Load the image and resize it
    image = Image.open('asset/logo 1 (3).png')
    image = image.resize(new_size)

    col1, col2 = st.columns(2, vertical_alignment="center")

    with col1:
        st.image(image, width=120)

    with col2:
        st.write('# Stylfit', unsafe_allow_html=True)

    st.write('# Chats History')
    if st.session_state.get('chat_id') is None:
        st.session_state.chat_id = st.selectbox(
            label='Choose past chat',
            options=[new_chat_id] + list(past_chats.keys()),
            format_func=lambda x: past_chats.get(x, 'New Chat'),
            placeholder='_',
        )
    else:
        # This will happen the first time AI response comes in
        st.session_state.chat_id = st.selectbox(
            label='Choose past chat',
            options=[new_chat_id, st.session_state.chat_id] + list(past_chats.keys()),
            index=1,
            format_func=lambda x: past_chats.get(x, 'New Chat' if x != st.session_state.chat_id else st.session_state.chat_title),
            placeholder='_',
        )
    # Save new chats after a message has been sent to AI
    # TODO: Give user a chance to name chat
    st.session_state.chat_title = f'ChatSession-{st.session_state.chat_id}'
    uploaded_file = st.file_uploader("Choose an image/video...", type=["jpg", "jpeg", "png", "mp4", "webp"], accept_multiple_files=True)
    st.caption('*Please after uploading an image or video and making a query, remove the file from the list to avoid uploading the same image/video again*')




st.write('# Chat with Stylfit 🧙‍♀️ ')
st.write("Don't know what to wear? Stylfit got you covered!!! ")

# Chat history (allows to ask multiple questions)
try:
    st.session_state.messages = joblib.load(
        f'data/{st.session_state.chat_id}-st_messages'
    )
    st.session_state.gemini_history = joblib.load(
        f'data/{st.session_state.chat_id}-gemini_messages'
    )
    print('old cache')
except:
    st.session_state.messages = []
    st.session_state.gemini_history = []
    print('new_cache made')

st.session_state.model = genai.GenerativeModel(model_name='gemini-1.5-flash', tools=[get_weather, search_web], system_instruction=persona, safety_settings=safety_settings_high)
st.session_state.chat = st.session_state.model.start_chat(
    history=st.session_state.gemini_history,
    enable_automatic_function_calling=True
)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(
        name=message['role'],
        avatar=USER_AVATAR_ICON if message['role'] == 'user' else AI_AVATAR_ICON,
    ):
        st.markdown(message['content'])

# React to user input
if prompt := st.chat_input('Your message here...'):
    # Save this as a chat for later
    if st.session_state.chat_id not in past_chats.keys():
        past_chats[st.session_state.chat_id] = st.session_state.chat_title
        joblib.dump(past_chats, 'data/past_chats_list')
    # Display user message in chat message container
    with st.chat_message(
        name='user',
        avatar=USER_AVATAR_ICON):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append(
        dict(
            role='user',
            content=prompt,
            avatar=USER_AVATAR_ICON
        )
    )
    # Send message to AI
    try:
        uploaded_files = []
        for image in uploaded_file:
            if image.name:
                uploaded_file = upload_to_gemini(image)
                uploaded_files.append(uploaded_file)
        if uploaded_files:
            message_args = []
            for i in range(len(uploaded_files)):
                message_args.append(uploaded_files[i])
            message_args.append(prompt)
            response = st.session_state.chat.send_message(
                message_args
            )
            uploaded_files.clear()
            uploaded_files.clear()
        else:
            response = st.session_state.chat.send_message(
                prompt
            )
        # Display assistant response in chat message container
        with st.chat_message(
            name=MODEL_ROLE,
            avatar=AI_AVATAR_ICON,
        ):
            message_placeholder = st.empty()
            full_response = ''
            assistant_response = response
            # Streams in a chunk at a time
            for chunk in response:
                # Simulate stream of chunk
                # TODO: Chunk missing `text` if API stops mid-stream ("safety"?)
                for ch in chunk.text.split(' '):
                    full_response += ch + ' '
                    time.sleep(0.05)
                    # Rewrites with a cursor at end
                    message_placeholder.write(full_response + '▌')
            # Write full message with placeholder
            message_placeholder.write(full_response)
    except Exception as e:
        advice = f"An error occurred: {str(e)}"

    # Add assistant response to chat history
    st.session_state.messages.append(
        dict(
            role=MODEL_ROLE,
            content=st.session_state.chat.history[-1].parts[0].text,
            avatar=AI_AVATAR_ICON,
        )
    )
    st.session_state.gemini_history = st.session_state.chat.history
    # Save to file
    joblib.dump(
        st.session_state.messages,
        f'data/{st.session_state.chat_id}-st_messages',
    )
    joblib.dump(
        st.session_state.gemini_history,
        f'data/{st.session_state.chat_id}-gemini_messages',
    )
