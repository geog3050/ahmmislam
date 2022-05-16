def hawkid():
    return(["A H M Mainul Islam", "ahmmislam"])

def import_data(filename):
    import re
    participants= []
    checkcol = False
    with open(filename) as f:
        if filename.endswith('.csv'):
            for val in f.readlines():
                val = val.strip()
                val = val.replace("\n","")
                val = val.split(',')
                participants.append(val)
            for d in participants:
                d[2]=float(d[2])
                d[3]=float(d[3])
        else:
            val = f.readlines()[1]
            val = re.split(r', |\[|\]',val)
            for element in val:
                if element.isdigit():
                    participants.append(int(element))
                  
    return participants

def attack_multiplier(attacker_type, defender_type):
    if attacker_type == "Water" and defender_type == "Fire":
            return 2.5
    elif attacker_type == "Electric" and defender_type == "Water":
            return 1.3
    elif attacker_type == "Ground" and defender_type == "Electric":
            return 2
    elif attacker_type == "Fire" and defender_type == "Grass":
            return 3.0
    elif attacker_type == "Grass" and defender_type == "Water":
            return 1.5
    else:
        return 1.0

def fight(participant1, participant2, first2attack):
    rounds = 0

    var1 = participant1[2]
    var2 = participant2[2]

    while var1 > 0 and var2 > 0:

        if first2attack == 1:
            n = attack_multiplier(participant1[1], participant2[1])
            new_attack_damage = n * participant1[3]
            var2 = var2 - new_attack_damage

        elif first2attack == 2:
            n = attack_multiplier(participant2[1], participant1[1])
            new_attack_damage = n * participant2[3]
            var1 = var1 - new_attack_damage

        rounds = rounds + 1

        if first2attack == 1:
            first2attack = 2
        else: 
            first2attack = 1

    if var1 > 0:
        return [1, rounds]
    elif var2 > 0:
        return [2, rounds]

def tournament(participants):

    wins = [0] * len(participants)
    
    for i in range(len(participants)):
        for p in range(i + 1, len(participants)):

           home_game = fight(participants[i], participants[p], 1)
           away_game = fight(participants[i], participants[p], 2)

           if home_game[0] == 1:
               wins[i] = wins[i] + 1
           elif home_game[0] == 2:
               wins[p] = wins[p] + 1

           if away_game[0] == 1:
               wins[i] = wins[i] + 1
           elif away_game[0] == 2:
               wins[p] = wins[p] + 1
    return wins
