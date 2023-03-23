import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import preprocessor
import analysis as ana



st.sidebar.title("Whatsapp Chat Analyzer")
uploader=st.sidebar.file_uploader("Upload File", type=['txt'], accept_multiple_files= False)

if  uploader is not None:
    data=uploader.getvalue().decode('utf-8')    
    
    df=preprocessor.preprocess(data)
    v1= st.title("Whatsapp Chat")
    v2= st.dataframe(df)



    user_list= df['user'].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()

    v3= st.header("Total Members")
    v4= st.title(len(user_list))


    user_list.insert(0,"Overall")



    selected_user=st.sidebar.selectbox("Chat Analysis",user_list)

    if st.sidebar.button('Show Analysis'):
        
        v1.empty()
        v2.empty()
        v3.empty()
        v4.empty()

   

        user_df= ana.dataframe(selected_user, df)
        st.title("Selected User's Chats")
        st.dataframe(user_df)
        st.title("Selected User's Statistic")
        num_messages, words, num_media, links = ana.fetch_stats(selected_user,df)

        col1, col2, col3, col4= st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Total Media")
            st.title(num_media)

        with col4:
            st.header("Total Links")
            st.title(links)

        if user_df.empty:
            st.header("Non Active User")
        else:
            st.title("Monthly Timeline")
            timeline_df= ana.monthly_timeline(selected_user, df)
            fig, ax= plt.subplots()
            plt.bar(timeline_df['time'],timeline_df['message'],width=0.5)
            ax.set_xlim(-0.5,5)
            plt.xlabel("Month")
            plt.ylabel("Frequency of message")
            plt.xticks(rotation=45)
            st.pyplot(fig)
            
            st.title("Daily Timeline")
            daily_timeline_df= ana.daily_timeline(selected_user, df)
            fig, ax= plt.subplots()
            plt.scatter(daily_timeline_df['date'],daily_timeline_df['message'], color='orange')
            plt.xlabel("Days")
            plt.ylabel("Frequency of message")
            plt.xticks(rotation=45)
            st.pyplot(fig)
        
            st.title("Activity Map")
            col1, col2= st.columns(2)
            
            with col1:
                st.header('Most Busy Day')
                busy_day=ana.weekly_activity(selected_user, df)
            
                fig, ax= plt.subplots()
                ax.bar(busy_day.index, busy_day.values, color='red',width=0.5)
                ax.set_xlim(-0.5,5)
                plt.xlabel("Day")
                plt.ylabel("Frequency of message")
                plt.xticks(rotation=45)
                st.pyplot(fig)
                
            with col2:
                st.header('Most Busy Month')
                busy_month=ana.month_activity(selected_user, df)
            
                fig, ax= plt.subplots()
                ax.bar(busy_month.index, busy_month.values, color='orange',width=0.5)
                ax.set_xlim(-0.5,5)
                plt.xlabel("Month")
                plt.ylabel("Frequency of message")
                plt.xticks(rotation=45)
                st.pyplot(fig)


            if selected_user =='Overall':
                st.title('Most Busy Users')
            
                x, new_df=ana.most_busy_user(df)
                fig, ax= plt.subplots()
            
                col1,col2 = st.columns(2)

                with col1:
                    ax.bar(x.index, x.values, color='green')
                    plt.xlabel("Users")
                    plt.ylabel("Frequency of message")
                    plt.xticks(rotation=45)
                    st.pyplot(fig)

                with col2:
                    st.dataframe(new_df)





            st.title('Most Common Words')
            common_df= ana.most_common_words(selected_user,df)

            col1,col2 = st.columns(2)

            with col1:
                fig, ax= plt.subplots()
                ax.bar(common_df[0], common_df[1])
                plt.xlabel("Common Words")
                plt.ylabel("Frequency of words")
                plt.xticks(rotation=45)
                st.pyplot(fig)

            with col2:
                st.dataframe(common_df)
        
        
            st.title('Common Emoji Used')
            emoji_df = ana.show_emoji(selected_user,df)
        
        
            if emoji_df.empty:
                st.write('No Emoji Used')
        
            else :
                col1,col2 = st.columns(2)
            
                with col1:
                    st.dataframe(emoji_df)
                
                with col2:
                    fig, ax= plt.subplots()
                    ax.pie(emoji_df[1], labels= emoji_df[0])
                    plt.legend(emoji_df[0], loc ="best")
                    st.pyplot(fig)

        
        