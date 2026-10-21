# dotnotes version
import pickle
import streamlit as st
# import time
import pandas as pd
#import numpy as np
import plotly.express as px
# from streamlit_plotly_events import plotly_events

def save_to_pickle(data, name):
    with open(name, 'wb') as file:
        pickle.dump(data, file)

def load_pickle(name):
    with open(name, 'rb') as file:
        return pickle.load(file)

def get_task_by_date(d, date1):
    ti = []
    for i in d.keys():
        if date1 in d[i]['Notes'].keys():
            ti.append(i)
    return ti
    
st.set_page_config(page_title="dotnotes", page_icon="📈", layout="wide")
# st.set_page_config(layout="wide")

st.title(':white_circle: dotNotes')  #'dotNotes'

from streamlit_lexical import streamlit_lexical

rich_text_dict = streamlit_lexical(value="initial value in **markdown**",
                             placeholder="Enter some rich text", 
                             height=800,
                             debounce=500,
                             key='1234', 
                             on_change=None
                            )


st.markdown(rich_text_dict)

## 'c:/users/l_yin/.spyder-py3/notebook.pkl'
file_path = 'c:/users/l_yin/.spyder-py3/init notebook.pkl'
notebook = load_pickle(file_path)
# st.write(notebook)

all_tasks_df = pd.DataFrame(notebook).T.drop(columns='Notes')

notes_df_plot = pd.DataFrame()
for key, value in notebook.items():
    idf = pd.DataFrame(value['Notes']).T.reset_index()
    idf['Task'] = key
    idf['Start Date'] = value['Start Date']
    notes_df_plot = pd.concat([notes_df_plot, idf])
notes_df_plot = notes_df_plot.rename(columns={'index':'Date', 'text':'Notes'})
notes_df_plot = notes_df_plot.sort_values(['Date', 'Start Date', 'Task'])
notes_df_plot['Rank'] = notes_df_plot.groupby('Date').cumcount()+1
notes_df_plot['Hours'] = notes_df_plot['Hours'].astype(float)

# st.container()
# st.write(notes_df_plot)

#@st.dialog("Update Note")
def show_existing_note(selected_points):
    st.session_state['n_dt'] = selected_points['points'][0]['x']
    st.session_state['n_tk'] = selected_points['points'][0]["legendgroup"]
    st.session_state['n_txt'] =  notebook[st.session_state['n_tk']]['Notes'][st.session_state['n_dt']]['text']
    st.session_state['n_ms'] =  notebook[st.session_state['n_tk']]['Notes'][st.session_state['n_dt']]['Milestone']
    st.session_state['n_hm'] =  notebook[st.session_state['n_tk']]['Notes'][st.session_state['n_dt']]['Home']
    st.session_state['n_hr'] =  notebook[st.session_state['n_tk']]['Notes'][st.session_state['n_dt']]['Hours']

    # t1 = st.container(key=21)
    # ed1, ed2, ed3, ed4, ed5, ed6, ed7 =t1.columns([2,1,7,1,1,1,1])
    # ed1.write('Task')
    # ed2.write('Date')
    # ed3.write('Note')
    # ed4.write('Hours')
    # ed5.write('Milestone')
    # ed6.write('Home')
        
    c1 = st.container(key=1)
    ed1, ed2, ed3, ed4, ed5, ed6, ed7 =c1.columns([2,1,7,1,1,1,2])

    ed1.write(st.session_state['n_tk'])
    ed2.write(st.session_state['n_dt'])
    
    st.session_state['n_txt'] = ed3.text_input('Notes', value=st.session_state['n_txt'], label_visibility="collapsed")
    st.session_state['n_hr'] = ed4.number_input('Hours', min_value=0.5, max_value=8.0, step=0.5, 
                                                value=float(st.session_state['n_hr']), label_visibility="collapsed")
    st.session_state['n_ms'] = ed5.checkbox('Milestone', value=st.session_state['n_ms'])
    st.session_state['n_hm'] = ed6.checkbox('Home', value=st.session_state['n_hm'])
    if ed7.button("Update Note", type="secondary", icon=":material/mood:", key=11):
        notebook[st.session_state['n_tk']]['Notes'][st.session_state['n_dt']]= {'text': st.session_state['n_txt'],
        'Milestone': st.session_state['n_ms'],
        'Home': st.session_state['n_hm'],
        'Hours': st.session_state['n_hr']}
        save_to_pickle(notebook, file_path)
        selected_points = None
        st.rerun()
    
    # t2 = st.container(key=22)
    # td1, td2, td3, td4, td5, td6, td7, td8 =t2.columns([2,1,1,6,1,1,1,1])
    # td1.write('Task')
    # td2.write('Start Date')
    # td3.write('Due Date')
    # td4.write('Contact')
    # td5.write('Type')
    # td6.write('Status')
    # td7.write('Priority')
    
    c2 = st.container(key=2)
    td1, td2, td3, td4, td5, td6, td7, td8 =c2.columns([2,1,1,6,1,1,1,2])

    tn = td1.text_input('Task Name',  value=st.session_state['n_tk'], label_visibility="collapsed")
    tsd = td2.date_input('Start Date', value=notebook[st.session_state['n_tk']]['Start Date'], label_visibility="collapsed")
    tdd = td3.date_input('Due Date', value=None if notebook[st.session_state['n_tk']]['Due Date']=="" else notebook[st.session_state['n_tk']]['Due Date'], 
                         label_visibility="collapsed")
    tc = td4.text_input('Contact', value=notebook[st.session_state['n_tk']]['Contact'], label_visibility="collapsed")
    tt = td5.selectbox('Type', options=['BI', 'DS', 'External', 'Misc'], 
                             index=['BI', 'DS', 'External', 'Misc'].index(notebook[st.session_state['n_tk']]['Type'])
                             , label_visibility="collapsed")
    ts = td6.selectbox('Status', options=['Queue', 'WIP', 'Park', 'Done', 'Delete'], 
                             index=['Queue', 'WIP', 'Park', 'Done', 'Delete'].index(notebook[st.session_state['n_tk']]['Status'])
                             , label_visibility="collapsed")
    tp = td7.number_input('Priority', min_value =1, max_value=5, step=1,
                                value=notebook[st.session_state['n_tk']]['Priority'], label_visibility="collapsed")
    if td8.button("Update Task", type="secondary", icon=":material/mood:", key=12):
        notebook[tn] = notebook.pop(st.session_state['n_tk'])
        notebook[tn]["Start Date"] = tsd.strftime('%Y-%m-%d')
        notebook[tn]['Due Date'] = tdd.strftime('%Y-%m-%d')
        notebook[tn]['Contact'] = tc
        notebook[tn]['Type'] = tt
        notebook[tn]["Status"] = ts
        notebook[tn]['Priority']= tp
        save_to_pickle(notebook, file_path)
        st.rerun()
    # st.session_state['n_dt'] = selected_points[0]['x']
    # y = selected_points[0]['y']
    # st.session_state['n_tk'] = notes_df_plot[(notes_df_plot['Date']==st.session_state['n_dt']) & (notes_df_plot['Rank']==y)]['Task'].to_list()[0]
    # st.session_state['n_txt'] =  notebook[st.session_state['n_tk']]['Notes'][st.session_state['n_dt']]['text']
    # st.session_state['n_ms'] =  notebook[st.session_state['n_tk']]['Notes'][st.session_state['n_dt']]['Milestone']
    # st.session_state['n_hm'] =  notebook[st.session_state['n_tk']]['Notes'][st.session_state['n_dt']]['Home']
    # st.session_state['n_hr'] =  notebook[st.session_state['n_tk']]['Notes'][st.session_state['n_dt']]['Hours']
    # form_task = st.form("task_form", border=False)
    # form_task.write(st.session_state['n_tk'])
    # form_task.write(st.session_state['n_dt'])
    # st.session_state['n_hr'] = form_task.number_input('Hours', min_value=0.5, max_value=8.0, step=0.5, 
    #                                             value=float(st.session_state['n_hr']))
    # st.session_state['n_ms'] = form_task.checkbox('Milestone', value=st.session_state['n_ms'], key=1)
    # st.session_state['n_hm'] = form_task.checkbox('Home', value=st.session_state['n_hm'], key=2)
    # st.session_state['n_txt'] = form_task.text_area('Notes', height=300, value=st.session_state['n_txt'])
    # if form_task.form_submit_button("Update", type="secondary", icon=":material/mood:"):
    #     notebook[st.session_state['n_tk']]['Notes'][st.session_state['n_dt']]= {'text': st.session_state['n_txt'],
    #     'Milestone': st.session_state['n_ms'],
    #     'Home': st.session_state['n_hm'],
    #     'Hours': st.session_state['n_hr']}
    #     save_to_pickle(notebook, 'c:/users/l_yin/.spyder-py3/notebook.pkl')
    #     selected_points = None
    #     st.rerun()
    

@st.dialog("Create New Task")
def show_new_task():
    form_task = st.form("task_form", border=False)
    tn = form_task.text_input('New Task Name')
    tsd = form_task.date_input('Start Date', value="today")
    tdd = form_task.date_input('Due Date', value=None)
    tc = form_task.text_input('Contact',)
    tt = form_task.selectbox('Type', options=['BI', 'DS', 'External', 'Misc'])
    ts = form_task.selectbox('Status', options=['Queue', 'WIP', 'Park', 'Done', 'Delete'])
    tp = form_task.number_input('Priority', min_value =1, max_value=5, step=1, value=1)
    ti = form_task.text_input('Initial Note', value='Task created.')
    if form_task.form_submit_button("Submit"):
        notebook[tn] = {"Start Date": tsd.strftime('%Y-%m-%d'), 'Due Date': tdd.strftime('%Y-%m-%d'), 
                        'Contact': tc, 'Type': tt,
                        "Status": ts, 'Priority': tp, 
                        'Notes': {tsd.strftime('%Y-%m-%d'): {'text': ti, 'Milestone':False,
                                                             'Home': True, 'Hours': 0.5}}}
        save_to_pickle(notebook, file_path)
        st.rerun()
    
# @st.dialog("Update Task")
# def show_existing_task():
#     form_task = st.form("task_form", border=False)
#     tn = form_task.text_input('Task Name',  value=st.session_state['n_tk'])
#     tsd = form_task.date_input('Start Date', value=notebook[st.session_state['n_tk']]['Start Date'])
#     tdd = form_task.date_input('Due Date', value=notebook[st.session_state['n_tk']]['Due Date'])
#     tc = form_task.text_input('Contact', value=notebook[st.session_state['n_tk']]['Contact'])
#     tt = form_task.selectbox('Type', options=['BI', 'DS', 'External', 'Misc'], 
#                              index=['BI', 'DS', 'External', 'Misc'].index(notebook[st.session_state['n_tk']]['Type']))
#     ts = form_task.selectbox('Status', options=['Queue', 'WIP', 'Park', 'Done', 'Delete'], 
#                              index=['Queue', 'WIP', 'Park', 'Done', 'Delete'].index(notebook[st.session_state['n_tk']]['Status']))
#     tp = form_task.number_input('Priority', min_value =1, max_value=5, step=1,
#                                 value=notebook[st.session_state['n_tk']]['Priority'])
#     if form_task.form_submit_button("Submit"):
#         notebook[tn] = notebook.pop(st.session_state['n_tk'])
#         notebook[tn]["Start Date"] = tsd
#         notebook[tn]['Due Date'] = tdd
#         notebook[tn]['Contact'] = tc
#         notebook[tn]['Type'] = tt
#         notebook[tn]["Status"] = ts
#         notebook[tn]['Priority']= tp
#         save_to_pickle(notebook, 'c:/users/l_yin/.spyder-py3/notebook.pkl')
#         st.rerun()


@st.dialog("New Note")
def show_new_note():
    nd = st.date_input('Date', value="today", key='newd')
    nt = st.selectbox('Task', options=list(set(notebook.keys()) - set(get_task_by_date(notebook, nd.strftime('%Y-%m-%d')))), key='newt')
    ns = st.number_input('Hours', min_value =0.5, max_value=8.0, step=0.5, value=0.5, key='newh')
    nm = st.checkbox('Milestone', key='ms')
    nh = st.checkbox('Home', key='h')
    nn = st.text_area('Note', height=300, key='newtxt')
    if st.button("Submit", key='newsub'):
        notebook[nt]['Notes'][nd.strftime('%Y-%m-%d')] = {'text': nn, 'Milestone': nm, 'Home': nh, 'Hours': ns}
        save_to_pickle(notebook, file_path)
        st.rerun()


### Create Dot Chart #########
fig = px.scatter(notes_df_plot, x="Date", y="Rank", color='Task', 
                 size='Hours',
                 template='plotly_dark', 
                 #marker_size=10,
                 #width=800, height=400
                 custom_data=['Task', 'Date', 'Notes']
                 )
fig.update_layout(
    yaxis_visible=False,
    yaxis=dict(
        showline=False,
        showticklabels=False,
        zeroline=False,
        showgrid=False,
    ),
    plot_bgcolor='rgb(14,17,23)',
    paper_bgcolor ='rgb(14,17,23)',
    #xaxis_visible=False,
    xaxis=dict(showgrid=False,
    title=None,
    type='date',
    tickformat='%b %d, %y %a',  # Format: Year-Month-Day
    #nticks=5
    ),
)

fig.update_traces(hovertemplate='<b>%{customdata[0]}</b><br><b>%{customdata[1]}</b><br>Note: %{customdata[2]}<extra></extra>')

# fig.update_traces(marker_size=20)
with st.container(height = 500, key=0):
    event = st.plotly_chart(fig, key="iris", on_select="rerun", config={'displayModeBar': False})
# st.write(event.selection)

# 
#     st.session_state['selected_points'] = plotly_events(fig, )
# # st.write(selected_points)
if event.selection['points']!=[]:
    show_existing_note(event.selection)
    # st.session_state['n_dt'] = selected_points[0]['x']
    # y = selected_points[0]['y']
    # st.session_state['n_tk'] = notes_df_plot[(notes_df_plot['Date']==st.session_state['n_dt']) & (notes_df_plot['Rank']==y)]['Task'].to_list()[0]
    # st.session_state['n_txt'] =  notebook[st.session_state['n_tk']]['Notes'][st.session_state['n_dt']]['text']
    # st.session_state['n_ms'] =  notebook[st.session_state['n_tk']]['Notes'][st.session_state['n_dt']]['Milestone']
    # st.session_state['n_hm'] =  notebook[st.session_state['n_tk']]['Notes'][st.session_state['n_dt']]['Home']
    # st.session_state['n_hr'] =  notebook[st.session_state['n_tk']]['Notes'][st.session_state['n_dt']]['Hours']
    
    # c1 = st.container(key=1)
    # ed1, ed2, ed3, ed4, ed5, ed6, ed7 =c1.columns([1,2,6,1,1,1,1])

    # ed1.write(st.session_state['n_dt'])
    # ed2.write(st.session_state['n_tk'])
    
    # st.session_state['n_txt'] = ed3.text_input('Notes', value=st.session_state['n_txt'], label_visibility="collapsed")
    # st.session_state['n_hr'] = ed4.number_input('Hours', min_value=0.5, max_value=8.0, step=0.5, 
    #                                             value=float(st.session_state['n_hr']), label_visibility="collapsed")
    # st.session_state['n_ms'] = ed5.checkbox('Milestone', value=st.session_state['n_ms'])
    # st.session_state['n_hm'] = ed6.checkbox('Home', value=st.session_state['n_hm'])
    # if ed7.button("Update", type="secondary", icon=":material/mood:"):
    #     notebook[st.session_state['n_tk']]['Notes'][st.session_state['n_dt']]= {'text': st.session_state['n_txt'],
    #     'Milestone': st.session_state['n_ms'],
    #     'Home': st.session_state['n_hm'],
    #     'Hours': st.session_state['n_hr']}
    #     save_to_pickle(notebook, 'c:/users/l_yin/.spyder-py3/notebook.pkl')
    #     selected_points = None
    #     st.rerun()

b1, b2, b3 = st.columns([1,1,12])
if b1.button("New Note", ):
    show_new_note()

if b2.button("New Task"):
    show_new_task()

te = b3.expander('All Tasks', icon=":material/add_box:")
te.dataframe(all_tasks_df)

# if b4.button('Refresh'):
#     st.session_state['selected_points'] = None
#     st.rerun()
# if st.button("Update Task"):
#     show_existing_task()

    

# st.write(notebook)
# ### Create New Tab ####
# col1, col2 = st.columns([1,3])
# ## create new task ##
# expander1 = col1.expander("Create A New Task", icon=":material/add_box:")
# form_task = expander1.form("task_form", border=False)
# tn = form_task.text_input('New Task Name')
# tsd = form_task.date_input('Start Date', value="today")
# tdd = form_task.date_input('Due Date', value=None)
# tc = form_task.text_input('Contact',)
# tt = form_task.selectbox('Type', options=['BI', 'DS', 'External', 'Misc'])
# ts = form_task.selectbox('Status', options=['Queue', 'WIP', 'Park', 'Done', 'Delete'])
# tp = form_task.number_input('Priority', min_value =1, max_value=5, step=1, value=1)
# tsub = form_task.form_submit_button("Submit")

# new_task = pd.DataFrame(
#     [
#      {"Task": tn, "Start Date": tsd, "Due Date": tdd,
#       "Contact": tc, 'Type': tt, 'Status': ts, 'Priority': tp},
#      ]
#     )
# if tsub:
#     tasks_df = pd.concat([tasks_df , new_task])
#     tasks_df.to_csv('c:/users/l_yin/.spyder-py3/tasks.csv', index=False)
# ## create new note ##
# expander2 = col2.expander("Create A New Note", icon=":material/add_box:")
# form_note = expander2.form("note_form", border=False)
# fn1, fn2, fn3, fn4, fn5, fn6 = form_note.columns([1,2,1,3,1,1])
# nd = fn1.date_input('Date', value="today")
# nt = fn2.selectbox('Task', options=list(set(tasks_df.Task.to_list())-set(notes_df[notes_df['Date']==pd.to_datetime(nd)]['Task'].to_list())))
# ns = fn3.number_input('Hours', min_value =0.5, max_value=8.0, step=0.5, value=0.5)
# nm = fn5.checkbox('Milestone')
# nh = fn6.checkbox('Home')
# nn = form_note.text_area('Note', height=300)

# nsub = form_note.form_submit_button("Submit")
# new_df = pd.DataFrame(
#     [
#        {"Date": pd.to_datetime(nd), "Task": nt, "Notes": nn, 
#         "Milestone": nm, "Home": nh, 'Hours': ns},
#    ]
# )
# if nsub:
#     notes_df = pd.concat([notes_df, new_df])
#     notes_df.to_csv('c:/users/l_yin/.spyder-py3/notes.csv', index=False)
    

# st.write(nd)



