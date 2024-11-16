import requests
# body = {
#     "difficulty": "easy", # "easy", "medium", or "hard" (defaults to "easy")
#     # "solution": True, # True or False (defaults to True)
#     "array": True # True or False (defaults to False)
# }
# headers =  {"Content-Type":"application/json"}

# response = requests.post("https://youdosudoku.com/api/", json=body, headers=headers)
# # response = requests.get("https://youdosudoku.com/api/")

# board = response.json()['puzzle']
# print("Board: ",board)
apiURL = "https://sugoku.onrender.com/board?difficulty=easy"
response = requests.get(apiURL)
# print("Response: ",response.json())
sudoku_board = response.json()['board']
print(sudoku_board)