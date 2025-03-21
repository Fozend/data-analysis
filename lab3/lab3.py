import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Завантаження даних
def load_data(file_path):
    # Перевірка наявності файлу
    if not os.path.exists(file_path):
        st.error(
            "File not found! Please check the following:\n"
            "1. Ensure you run script in the root directory of the repository\n"
            "2. Ensure you have run the cells in lab2.ipynb or executed lab2.py"
        )
        return None
    else:
        data = pd.read_csv(file_path)
        return data

def reset_filters():
    st.session_state["selected_option"] = 'VCI'
    st.session_state["selected_region"] = data['Region'].unique()[0]
    st.session_state["year_range"] = (int(data["Year"].min()), int(data["Year"].max()))
    st.session_state["week_range"] = (int(data["Week"].min()), int(data["Week"].max()))
    st.session_state["sort_asc"] = False
    st.session_state["sort_desc"] = False

file_path = os.path.join('lab2', 'VHI_data', 'NOAA_Ukraine_Updated.csv')
data = load_data(file_path)

data["Week"] = data["Week"].astype(int)
data["Year"] = data["Year"].astype(int)

region_names = {
    1: "Вінницька",
    2: "Волинська",
    3: "Дніпропетровська",
    4: "Донецька",
    5: "Житомирська",
    6: "Закарпатська",
    7: "Запорізька",
    8: "Івано-Франківська",
    9: "Київ",
    10: "Київcька",
    11: "Кіровоградська",
    12: "Луганська",
    13: "Львівська",
    14: "Миколаївська",
    15: "Одеська",
    16: "Полтавська",
    17: "Рівненська",
    18: "Севастополь",
    19: "Сумська",
    20: "Тернопільська",
    21: "Харківська",
    22: "Херсонська",
    23: "Хмельницька",
    24: "Черкаська",
    25: "Чернівецька",
    26: "Чернігівська",
    27: "Республіка Крим"
}

if data is not None:
    st.title('Data Analysis: VCI, TCI, VHI')

    # Колонки
    col1, col2 = st.columns([2,3])

    with col1:
        # Ініціалізація session_state
        st.session_state.setdefault("selected_option", 'VCI')
        st.session_state.setdefault("selected_region", data['Region'].unique()[0])
        st.session_state.setdefault("year_range", (int(data["Year"].min()), int(data["Year"].max())))
        st.session_state.setdefault("week_range", (int(data["Week"].min()), int(data["Week"].max())))
        st.session_state.setdefault("sort_asc", False)
        st.session_state.setdefault("sort_desc", False)

        # 1. Dropdown для вибору часових рядів
        options = ['VCI', 'TCI', 'VHI']
        selected_option = st.selectbox('Select Time Series:', options)

        st.session_state["selected_option"] = selected_option

        # 2. Dropdown для вибору області
        regions = list(region_names.values())
        if st.session_state["selected_region"] in regions:
            index = regions.index(st.session_state["selected_region"])
        else:
            index = 0

        selected_region = st.selectbox('Select Region:', regions, index=index)

        st.session_state["selected_region"] = selected_region

        # 3. Slider для вибору інтервалу тижнів
        min_week = data['Week'].min()
        max_week = data['Week'].max()
        
        # перевірка для призначення/скидання
        if 'week_range' in st.session_state:
            week_range = st.slider('Select Week range:', min_week, max_week, st.session_state['week_range'])
        else:
            week_range = st.slider('Select Year range:', min_week, max_week, (min_week, max_week))

        st.session_state["week_range"] = week_range

        # 4. Slider для вибору інтервалу років
        min_year = data['Year'].min()
        max_year = data['Year'].max()

        # перевірка для призначення/скидання
        if 'year_range' in st.session_state:
            year_range = st.slider('Select Year range:', min_year, max_year, st.session_state['year_range'])
        else:
            year_range = st.slider('Select Year range:', min_year, max_year, (min_year, max_year))

        st.session_state["year_range"] = year_range

        # Фільтрація даних за обраними параметрами
        region_index = next((key for key, value in region_names.items() if value == st.session_state["selected_region"]), None)
        filtered_data = data[
            (data['Year'] >=  st.session_state["year_range"][0]) &
            (data['Year'] <=  st.session_state["year_range"][1]) &
            (data['Week'] >= st.session_state["week_range"][0]) &
            (data['Week'] <= st.session_state["week_range"][1]) &
            (data['Region'] == region_index)
        ]

        # 8. Два checkbox для сортування даних
        st.session_state['sort_asc'] = st.checkbox('Sort data in Ascending Order', value=st.session_state["sort_asc"])
        st.session_state["sort_desc"] = st.checkbox('Sort data in Descending Order', value=st.session_state["sort_desc"])

        # if 'sort_asc' in st.session_state:
        #     sort_asc = st.session_state['sort_asc']
        # else:
        #     sort_asc = False
            
        # st.session_state["sort_asc"] = sort_asc

        # if 'sort_desc' in st.session_state:
        #     sort_desc = st.session_state['sort_desc']
        # else:
        #     sort_desc = False

        # st.session_state["sort_desc"] = sort_desc

        if st.session_state["sort_asc"] and st.session_state["sort_desc"]:
            st.warning("Both sort options selected. Only ascending will be applied.")
        elif st.session_state["sort_asc"]:
            filtered_data = filtered_data.sort_values(by=st.session_state["selected_option"], ascending=True)
        elif st.session_state["sort_desc"]:
            filtered_data = filtered_data.sort_values(by=st.session_state["selected_option"], ascending=False)

        # 5. Button для скидання фільтрів
        st.button('Reset Filters', on_click=reset_filters)

    with col2:
        # Tabs для таблиці та графіка з відфільтрованими даними, графіка порівнянь даних по областях
        tab1, tab2, tab3 = st.tabs(["Filtered Data Table", "Time Series Plot", "Region Comparison"])

        #  Таблиця з відфільтрованими даними
        with tab1:
            st.write(filtered_data)

        # Графік з відфільтрованими даними
        with tab2:
            plt.figure(figsize=(6, 3)) 
            sns.lineplot(x=filtered_data["Year"], y=filtered_data[st.session_state["selected_option"]])
            plt.title(f"Time Series {st.session_state['selected_option']} for {st.session_state['selected_region'] } region")
            years = sorted(filtered_data["Year"].unique())
            step = 3
            selected_years = years[::step] 
            plt.xticks(selected_years, rotation=90)
            st.pyplot(plt)

        # Графік порівняння даних по областях
        with tab3:
            comparison_data = data[
                (data['Year'] >= st.session_state["year_range"][0]) & (data['Year'] <= st.session_state["year_range"][1]) &
                (data['Week'] >= st.session_state["week_range"][0]) & (data['Week'] <= st.session_state["week_range"][1])
            ]
            comparison_data_grouped = comparison_data.groupby('Region')[st.session_state["selected_option"]].mean()

            # Заміна індексіви на відповідні назви регіонів
            comparison_data_grouped.index = comparison_data_grouped.index.map(region_names)
    
            plt.figure(figsize=(6, 3)) 
            sns.barplot(x=comparison_data_grouped.index, y=comparison_data_grouped.values, palette="bright")
            plt.xticks(rotation=90)
            plt.xlabel('Region')
            plt.ylabel(f'Average {st.session_state["selected_option"]}')
            plt.title(f"Average {st.session_state['selected_option']} by Region") 
            
            # Виведення графіку на сторінці
            st.pyplot(plt)