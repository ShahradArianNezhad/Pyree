
import graphviz

dot = graphviz.Digraph()
dot.attr(rankdir='TB')

binding_powers = {
    "+":1,
    "-":1,
    "*":2,
    "/":2,
    "(":3,
    ")":3,
}

def lexer(expr:str):
    start_win_op=None
    start_win_brace=None
    open_braces_seen=0
    flag=False
    close_braces_seen=0
    tokens = list()
    for i in range(len(expr)):
        if start_win_brace ==None:
            if i==0: 
                if expr[i]=='(':
                    start_win_brace=i
                    open_braces_seen+=1
                    continue
                tokens.append(["digit",expr[i]])
                continue
            if expr[i].isnumeric():
                if i==len(expr)-1:
                    if start_win_op==None:
                        tokens.append(["digit",expr[i]])
                        continue
                    else:
                        tokens.append(["expression",expr[start_win_op:i+1]])
                        continue
                if binding_powers[expr[i+1]] > binding_powers[expr[i-1]]:
                    if start_win_op==None:
                        start_win_op=i
                elif binding_powers[expr[i+1]] < binding_powers[expr[i-1]]:
                    tokens.append(["expression",expr[start_win_op:i+1]])
                    if start_win_op!=None:
                        start_win_op=None
                    else:
                        flag=True
                # elif i+2<len(expr) and expr[i+2]=="(":

                else:
                    if start_win_op==None:
                        tokens.append(["digit",expr[i]])
            else:
                if expr[i]=='(':
                    start_win_brace=i
                    open_braces_seen+=1
                    continue
                if start_win_op==None:
                    tokens.append(["operator",expr[i]])  
        elif(expr[i]==')'):
            if(open_braces_seen==close_braces_seen+1):   
                if start_win_op==None:
                    tokens.append(["expression",expr[start_win_brace:i+1]])
                else:
                    tokens.append(["expression",expr[start_win_op:i+1]])
                    start_win_op=None
                open_braces_seen=0
                close_braces_seen=0
                start_win_brace=None
            else:
                close_braces_seen+=1
        elif(expr[i]=='('):
            open_braces_seen+=1
         
    if flag:
        tokens.pop(0)
        tokens.pop(0)

    for i in range(len(tokens)):
        if tokens[i][0]=="expression":
            if(tokens[i][1][0]=="(" and tokens[i][1][-1]==")"):
                tokens[i][1]=tokens[i][1][1:-1]
            tokens[i][1]=lexer(tokens[i][1])

    return tokens            

def calculate(d1:int|float,d2:int|float,op):
    if(op=="*"):
        return d1*d2
    elif(op=="/"):
        return d1/d2
    elif(op=="-"):
        return d1-d2
    elif(op=="+"):
        return d1+d2


def parse(tokens:list,dot:graphviz.Digraph):
    d1=d2=op=last_op_name=None

    for i,token in enumerate(tokens):
        if token[0]=="digit":
            if d1==None:
                dot.node(f"{id(token)}",f"{token[1]}")
                dot.edge(f"{id(tokens[i+1])}",f"{id(token)}")
                d1=int(token[1])
            else:
                d2=int(token[1])
                d1=calculate(d1,d2,op)
                dot.node(f"{id(token)}",f"{token[1]}")
                dot.edge(f"{id(tokens[i-1])}",f"{id(token)}")
                d2=None
                op=None
        elif token[0]=="operator":
            dot.node(f"{id(token)}",f"{token[1]}")
            op=token[1]
            if(last_op_name!=None):
                dot.edge(f"{id(token)}",last_op_name)
            last_op_name=f"{id(token)}"
        elif token[0]=="expression":
            if d1==None:
                x,d1=parse(token[1],dot)
                dot.edge(f"{id(tokens[i+1])}",x)
            else:
                x,d2=parse(token[1],dot)
                d1=calculate(d1,d2,op)
                dot.edge(f"{id(tokens[i-1])}",x)
                d2=None
                op=None

    return [last_op_name,d1]







tokens = lexer(input().replace(" ",""))

print(tokens)

print(parse(tokens,dot)[1])


dot.render('my_graph.gv', format='pdf')