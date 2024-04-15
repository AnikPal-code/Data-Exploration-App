import os
import streamlit as st 
import pandas as pd 
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
import seaborn as sns 

def main():
    """ Common ML Dataset Explorer """
    st.title("Common ML Dataset Explorer")
    st.subheader("Datasets For ML Explorer with Streamlit")

    html_temp = """
    <div style="background-color:tomato;"><p style="color:white;font-size:50px;padding:10px">Data Informatics</p></div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

    def file_selector(folder_path='./datasets'):
        filenames = os.listdir(folder_path)
        selected_filename = st.selectbox("Select A file", filenames)
        return os.path.join(folder_path, selected_filename)

    filename = file_selector()
    st.info("You Selected {}".format(filename))

    df = pd.read_csv(filename)

    if st.checkbox("Show Dataset", key="show_dataset"):
        number = st.number_input("Number of Rows to View", min_value=5, step=1)
        st.dataframe(df.head(int(number)))

    if st.button("Column Names", key="column_names"):
        st.write(df.columns)

    if st.checkbox("Shape of Dataset", key="shape_dataset"):
        data_dim = st.radio("Show Dimension By ", ("Rows", "Columns"), key="data_dim")
        if data_dim == 'Rows':
            st.text("Number of Rows")
            st.write(df.shape[0])
        elif data_dim == 'Columns':
            st.text("Number of Columns")
            st.write(df.shape[1])
        else:
            st.write(df.shape)

    if st.checkbox("Select Columns To Show", key="select_columns"):
        all_columns = df.columns.tolist()
        selected_columns = st.multiselect("Select", all_columns)
        new_df = df[selected_columns]
        st.dataframe(new_df)
    
    if st.button("Value Counts", key="value_counts"):
        st.text("Value Counts By Target/Class")
        st.write(df.iloc[:, -1].value_counts())

    if st.button("Data Types", key="data_types"):
        st.write(df.dtypes)

    if st.checkbox("Summary", key="summary"):
        st.write(df.describe().T)

    st.subheader("Data Visualization")

    if st.checkbox("Correlation Plot[Seaborn]", key="correlation_plot"):
        correlation_plot = sns.heatmap(df.corr(), annot=True)
        st.pyplot(correlation_plot.figure)


    if st.checkbox("Pie Plot", key="pie_plot"):
    	if st.button("Generate Pie Plot", key="generate_pie_plot"):
       		st.success("Generating A Pie Plot")
        	pie_data = df.iloc[:, -1].value_counts()
        	fig, ax = plt.subplots()
        	ax.pie(pie_data, labels=pie_data.index, autopct="%1.1f%%")
        # Pass the figure object to st.pyplot()
        	st.pyplot(fig)



    if st.checkbox("Plot of Value Counts", key="plot_value_counts"):
        st.text("Value Counts By Target")
        all_columns_names = df.columns.tolist()
        primary_col = st.selectbox("Primary Column to GroupBy", all_columns_names)
        selected_columns_names = st.multiselect("Select Columns", all_columns_names)
        if st.button("Plot", key="plot_button"):
            st.text("Generate Plot")
            if selected_columns_names:
                vc_plot = df.groupby(primary_col)[selected_columns_names].count()
            else:
                vc_plot = df.iloc[:, -1].value_counts()
            st.write(vc_plot.plot(kind="bar"))
            st.pyplot()

    st.subheader("Customizable Plot")
    all_columns_names = df.columns.tolist()
    type_of_plot = st.selectbox("Select Type of Plot", ["area", "bar", "line", "hist", "box", "kde"], key="type_of_plot")
    selected_columns_names = st.multiselect("Select Columns To Plot", all_columns_names, key="select_columns_plot")

    if st.button("Generate Plot", key="generate_custom_plot"):
        st.success("Generating Customizable Plot of {} for {}".format(type_of_plot, selected_columns_names))

        if type_of_plot == 'area':
            cust_data = df[selected_columns_names]
            st.area_chart(cust_data)

        elif type_of_plot == 'bar':
            cust_data = df[selected_columns_names]
            st.bar_chart(cust_data)

        elif type_of_plot == 'line':
            cust_data = df[selected_columns_names]
            st.line_chart(cust_data)

        elif type_of_plot:
            cust_plot = df[selected_columns_names].plot(kind=type_of_plot)
            st.write(cust_plot)
            st.pyplot()

    if st.button("Thanks", key="thanks_button"):
        st.balloons()

    st.sidebar.header("About the App")
    st.sidebar.info("A simple user-friendly data explorer app to uncover all the information about your dataset.")

    st.sidebar.header("About")
    st.sidebar.text("Built with Streamlit @Python")
    st.sidebar.text("Created and Maintained by Anik Pal")

if __name__ == '__main__':
    main()
