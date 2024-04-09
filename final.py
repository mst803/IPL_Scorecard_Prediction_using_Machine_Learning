import pickle
import streamlit as st
from Dict import stadium_size,bat,ball,teams,team_

class Queue:
    def __init__(self):
        self.items=[]
    def is_empty(self):
        return self.items==[]
    def enqueue(self,item):
        self.items.insert(0,item)
    def dequeue(self):
        return self.items.pop()
    def peek(self):
        return self.items[-1]
    def size(self):
        return len(self.items)
    
#To add bowlers who are not in the batting
a=3
for i in ball:
    if i not in bat:
        bat[i]=a+0.5
        a+=1
st.title("IPL PREDICTION")
st.sidebar.title("Selected Players")
col1_sidebar, col2_sidebar = st.sidebar.columns(2)

col1, col2 = st.columns(2)
with col1:
    team_1=st.selectbox("Select the batting team",sorted(teams))

with col2:
    team_2_options = [team for team in sorted(teams) if team != team_1]
    team_2 = st.selectbox("Select the bowling team", team_2_options)


if not hasattr(st.session_state, "selected_players"):
    st.session_state.lineup_1 = {team: [] for team in teams}

# Display available players based on selected team_1
col1,col2 = st.columns(2)
with col1:
    if team_1:
        Availabe_players_1 = teams.get(team_1)
        st.write("Available Players for " + team_1)
        lineup_1 = st.multiselect("Select players", Availabe_players_1)

        # Limit selection to 11 players
        if len(lineup_1) != 11:
            st.warning("Please select only 11 players.")
            lineup_1 = lineup_1[:11]

        # Update session state
        st.session_state.lineup_1[team_1] = lineup_1

    # Display selected players in the sidebar for team_1
    with col1_sidebar:
        st.markdown("### " + team_1)
        if st.session_state.lineup_1.get(team_1):
            for player in st.session_state.lineup_1.get(team_1):
                st.write(player)
        else:
            st.write("No players selected yet.")

if not hasattr(st.session_state, "selected_players"):
    st.session_state.lineup_2 = {team: [] for team in teams}

with col2:
    if team_2:
        Availabe_players_2 = teams.get(team_2)
        st.write("Available Players for " + team_2)
        lineup_2 = st.multiselect("Select players", Availabe_players_2)

        # Limit selection to 11 players
        if len(lineup_2) != 11:
            st.warning("Please select 11 players.")
            lineup_2 = lineup_2[:11]

        # Update session state
        st.session_state.lineup_2[team_2] = lineup_2

    # Display selected players in the sidebar for team_1
    with col2_sidebar:
        st.markdown("### " + team_2)
        if st.session_state.lineup_2.get(team_2):
            for player in st.session_state.lineup_2.get(team_2):
                st.write(player)
        else:
            st.write("No players selected yet.")



stadium=st.selectbox("Select host city", sorted(stadium_size))
stadium=stadium_size[stadium]
Decision=["Batting","Bowling"]
Year=[i for i in range (2015,2026)]
col1,col2=st.columns(2)
with col1:
    toss=st.selectbox("Select toss decision",Decision)
    
with col2:
    Year=st.selectbox("Year",Year)
toss=toss=="Batting"

available_overs = list(range(1, 21))

st.title("Bowler Assignment")

col1, col2 = st.columns(2)

# First team bowlers
with col1:
    num_bowlers_team1 = st.number_input("Select the number of bowlers for Team 1:", min_value=1, max_value=10, value=1, step=1, key="num_bowlers_team1")
    bowlers_1 = {}
    
    for i in range(num_bowlers_team1):
        st.header(f"Team 2 - Bowler {i+1} Assignment")
        remaining_bowlers = [bowler for bowler in lineup_1 if bowler not in bowlers_1]
         
        selected_bowler = st.selectbox(f"Select bowler {i+1}:", remaining_bowlers, key=f"bowler_team1_{i}")
        if selected_bowler not in ball:
            st.error("Please select a bowler")
        remaining_overs = st.multiselect(f"Select overs for {selected_bowler}:", available_overs, key=f"overs_team1_{i}")
        if len(remaining_overs)>4:
            st.error("Select only 4 overs")
        available_overs = [over for over in available_overs if over not in remaining_overs]
        
        bowlers_1[selected_bowler] = remaining_overs

    st.header("Team 2 - Bowler Assignments")
    for bowler, overs in bowlers_1.items():
        st.write(f"{bowler}: Overs {', '.join(map(str, overs))}")

# Second team bowlers
available_overs = list(range(1, 21))
with col2:
    num_bowlers_team2 = st.number_input("Select the number of bowlers for Team 2:", min_value=1, max_value=10, value=1, step=1, key="num_bowlers_team2")
    bowlers_2 = {}
    
    for i in range(num_bowlers_team2):
        st.header(f"Team 1 - Bowler {i+1} Assignment")
        remaining_bowlers = [bowler for bowler in lineup_2 if bowler not in bowlers_2]
        selected_bowler = st.selectbox(f"Select bowler {i+1}:", remaining_bowlers, key=f"bowler_team2_{i}")
        if selected_bowler not in ball:
            st.error("Please select a bowler")
        remaining_overs = st.multiselect(f"Select overs for {selected_bowler}:", available_overs, key=f"overs_team2_{i}")
        if len(remaining_overs)>4:
            st.error("Select only 4 overs")
        available_overs = [over for over in available_overs if over not in remaining_overs]
        
        bowlers_2[selected_bowler] = remaining_overs

    st.header("Team 1 - Bowler Assignments")
    for bowler, overs in bowlers_2.items():
        st.write(f"{bowler}: Overs {', '.join(map(str, overs))}")
def main():
    bowlers_1_final=[0 for i in range(20)]
    for i,j in bowlers_1.items():
        for k in j:
            bowlers_1_final[k-1]=i
    
    bowlers_2_final=[0 for i in range(20)]
    for i,j in bowlers_2.items():
        for k in j:
            bowlers_2_final[k-1]=i
    bowling_1=[]
    for i in bowlers_1_final:
        try:
                b = ball[i]
                bowling_1.append(b)
        except KeyError:
            continue
    bowling_2=[]
    for i in bowlers_2_final:
        try:
            b=ball[i]
            bowling_2.append(b)
        except:
            continue


    Team_1=team_[team_1]
    Team_2=team_[team_2]

    with open("LF_1.pkl","rb") as f:
        LF_1=pickle.load(f)
    with open("RF_2.pkl","rb") as f:
        RF_2=pickle.load(f)

    def get_key(dictionary, target_value):
        keys_with_target_value =''
        for key, value in dictionary.items():
            if value == target_value:
                keys_with_target_value=key
                break
        return keys_with_target_value

    players_T1=Queue()
    players_T2=Queue()
    for i in lineup_1:
        j=bat[i]
        
        players_T1.enqueue(j)
    for i in lineup_2:
        j=bat[i]
        players_T2.enqueue(j)

    on_field=Queue()
    on_field.enqueue(players_T1.dequeue())
    on_field.enqueue(players_T1.dequeue())
    inn=1
    total_runs_1=0
    a_r=0
    b_r=0
    r_f=1

    six=0
    five=0
    four=0
    three=0
    two=0
    one=0
    zero=0

    all_out=False

    for j in range(len(bowling_2)):
        r_f_o=1
        if all_out:
            break
        for k in range(1,7):
            if (LF_1.predict_proba([[inn,j,k,stadium,toss,on_field.peek(),bowling_2[j],Team_1,Team_2,Year]])[:,1])*r_f*r_f_o>0.33:
                r_f=0.8
                r_f_o-=0.1
                a=on_field.dequeue()
                total_runs_1+=a_r
                st.write(get_key(bat,a),':',str(a_r),'\t',"&nbsp;","wicket taken by",get_key(ball,bowling_2[j]))
                a_r=0

                if players_T1.is_empty():
                    all_out=True
                    break
                on_field.enqueue(players_T1.dequeue())
                on_field.enqueue(on_field.dequeue())

            
                
            else:
                r_f=1
                b=RF_2.predict_proba([[inn,j,k,stadium,toss,on_field.peek(),bowling_2[j],Team_1,Team_2,Year]])

                for i in range(7):
                    if b[:,i]>0.37:
                        b=i
                        break
                else:
                    if b[:,4]>0.27:
                        b=4
                        four+=1
                        
                    elif b[:,6]>0.25:
                        b=6
                        six+=1
                        
                    elif b[:,3]>0.16:
                        b=3
                        
                        three+=1

                    elif b[:,5]>0.16:
                        b=5
                        
                        five+=1

                    elif b[:,2]>0.24:
                        b=2
                        
                        two+=1

                    elif b[:,1]>0.2:
                        b=1
                        
                        one+=1

                    else:
                        b=0

                        zero+=1
                
                a_r+=b


                if b%2==1:
                    on_field.enqueue(on_field.dequeue())
                    a_r,b_r=b_r,a_r

        
        if j!=19:
            on_field.enqueue(on_field.dequeue())
            a_r,b_r=b_r,a_r

            
             
    total_runs_1+=a_r+b_r
    if not all_out:
        st.write(get_key(bat,on_field.dequeue()),':',str(a_r),'\t','not out')
    st.write(get_key(bat,on_field.dequeue()),':',str(b_r),'\t','not out')
    st.write("Total runs =",str(total_runs_1),"+ Extras")



    st.write(six,five,four,three,two,one,zero)


    st.write("\n" + "="*60 + "\n",end='\n\n')

    on_field=Queue()
    on_field.enqueue(players_T2.dequeue())
    on_field.enqueue(players_T2.dequeue())

    inn=2
    total_runs=0
    a_r=0
    b_r=0
    r_f=1
    all_out=False

    six=0
    five=0
    four=0
    three=0
    two=0
    one=0
    zero=0

    for j in range(len(bowling_1)):
        r_f_o=1
        if all_out:
            break
        for k in range(1,7):
            if (LF_1.predict_proba([[inn,j,k,stadium,toss,on_field.peek(),bowling_1[j],Team_2,Team_1,Year]])[:,1])*r_f*r_f_o>0.32:
                r_f=0.8
                r_f_o-=0.1
                a=on_field.dequeue()
                total_runs+=a_r
                st.write(get_key(bat,a),':',str(a_r),'\t','&nbsp;',"wicket taken by",get_key(ball,bowling_1[j]))
                a_r=0
                if players_T2.is_empty():
                    all_out=True
                    break
                on_field.enqueue(players_T2.dequeue())
                on_field.enqueue(on_field.dequeue())
            


            else:
                r_f=1
                b=RF_2.predict_proba([[inn,j,k,stadium,toss,on_field.peek(),bowling_1[j],Team_2,Team_1,Year]])

                for i in range(7):
                    if b[:,i]>0.37:
                        b=i
                        break
                else:

                    if b[:,4]>0.27:
                        b=4
                        four+=1
                        
                    elif b[:,6]>0.25:
                        b=6

                        six+=1
                        
                    elif b[:,3]>0.16:
                        b=3
                        
                        three+=1

                    elif b[:,5]>0.16:
                        b=5
                        
                        five+=1

                    elif b[:,2]>0.24:
                        b=2
                        
                        two+=1

                    elif b[:,1]>0.2:
                        b=1
                        
                        one+=1

                    else:
                        b=0

                        zero+=1
                
                a_r+=b

                if b%2==1:
                    on_field.enqueue(on_field.dequeue())
                    a_r,b_r=b_r,a_r

            if total_runs+b_r>total_runs_1:
                st.write(str(get_key(team_,Team_2)),' Wins')
                break
        
        if j!=19:
            on_field.enqueue(on_field.dequeue())
            a_r,b_r=b_r,a_r

    total_runs+=a_r+b_r
    if not all_out:
        st.write(get_key(bat,on_field.dequeue()),':',str(a_r),'\t','not out')
    st.write(get_key(bat,on_field.dequeue()),':',str(b_r),'\t','not out')
    st.write("Total runs =",str(total_runs),"+ Extras")
    if total_runs+b_r<total_runs_1:
        st.write(str(get_key(team_,Team_1)),' Wins')

    st.write(six,five,four,three,two,one,zero)

predict_button=st.button("predict")
with st.spinner("Prediction takes a While"):
    if predict_button:
        main()
