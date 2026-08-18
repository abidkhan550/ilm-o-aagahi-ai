# 🚀 Ask Button
if st.button("🚀 Ask / جواب حاصل کریں"):
    if user_text or final_image:
        with st.spinner("Processing..."):
            contents_list = []
            if final_image:
                contents_list.append(final_image)
            if user_text:
                contents_list.append(user_text)
            elif final_image and not user_text:
                contents_list.append(f"Please read all educational content in this image and explain/solve it thoroughly in {target_language}.")

            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=contents_list,
                    config=types.GenerateContentConfig(
                        system_instruction=f"You are an expert AI educational tutor named Abid working for 'Ilm-o-Aagahi AI'. Strictly respond in {target_language}. Explain step-by-step.",
                    ),
                )
                st.success("Answer / جواب:")
                # رسپانس کو محفوظ طریقے سے دکھانے کے لیے
                if response and hasattr(response, 'text'):
                    st.markdown(response.text)
                else:
                    st.write("No response generated.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a question or attach an image first!")
