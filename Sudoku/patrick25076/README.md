# Stellar Sudoku
![Sudoku Game](https://scontent.fsbz3-1.fna.fbcdn.net/v/t39.30808-6/321349602_1340398730107080_7756720123638753800_n.jpg?_nc_cat=110&ccb=1-7&_nc_sid=730e14&_nc_ohc=RRVcyMbSuxEAX8zqtAO&_nc_ht=scontent.fsbz3-1.fna&oh=00_AfDmqbZ9HWMAyJG4E3854MfzzgAOPU6mZZU3Lzj4tQW2Ig&oe=63A6992E)
## Video Demo:  <https://www.youtube.com/watch?v=Sjrom7oYiwM>
## Explaining the project:
This is my CS50x final project which is a Sudoku Web Application.The app was developed with Python,Javascript,Flask Framework, HTML and CSS.
You start the game with 5 lives and 3 hints.
These are the features of the app:
- Generate Sudoku: This function generates a number of unlimited random sudoku grids using a backtracking algorithm in Python which is passed to JavaScript through AJAX.
- Hint: This function is revealing the correct value from the selected cell.
- Solve Sudoku: This function instantly solves the sudoku.
- Validate Sudoku: This function checks if the sudoku is valid.
- Lives: You get 5 lives at the beginning of every game.
- Numpad: This is the numpad from which you can pick the digit that suit in the selected cell, if we are done with one digit , the button for that respective digit will dissapear.
- Timer: Every time you start a new game the timer will start from 0.

## Python Usage(Sudoku Generator/Solve Algortihm Explained)
I started by creating a function that checks if a digit is valid on a certain column and row in a certain grid:
```python
        def isvalid(board,row,col,num):
    for x in range(9):
        if board[row][x]==num:
            return False
        if board[x][col]==num:
            return False
    startcol= col-col%3
    startrow=row-row%3
    for x in range(3):
        for y in range(3):
            if board[startrow+x][startcol+y]==num:
                return False
    return True
```
Firstly, this function checks if that digit exists in the same row, then the function checks if the digit exists in the same column
</hr>
and then the function checks if the digit exists in the same block. If the digit is valid on that certain position it will return True.

</hr>
Then, I initialize the solve function which uses recursion and backtracking method:

```python
    def solve(board,row,col):
    if col==9:
        if row==8:
            return True
        col=0
        row+=1
    if board[row][col]>0:
        return solve(board,row,col+1)
    for x in range(1,10):
        if isvalid(board,row,col,x):
            board[row][col]=x
            if solve(board,row,col+1):
                return True
        board[row][col]=0
    return False
```
Firstly, this function checks if the solving is done by seeing if all the columns and rows was completed. Then ,if a number does not have a value , we check with our previous function isvalid to see
if numbers 1 through 9 are valid in that certain place.If the number is valid , we check for the rest of the board to see if it fits even after all the board is filled.If it does not fit, the whole procces start again until the grid is filled with values.

</hr>
The last thing that I did to make the grids to be random was to add a function that put random values on an empty sudoku grid:

```python

    def randomize(board):
    for i in range(random.randint(2,5)):
        for j in range(random.randint(1,6)):
            val=random.randint(1,9)
            if isvalid(board,i,j,val):
                board[i][j]=val


```

With this function I create a random Sudoku Grid with a few values on it and then I solve it with the solve function, to have a full random grid, and after that I remove a random number of values to make it playable.

## Passing the Sudoku Grid to Javascript and HTML
Passing the Sudoku Grid to JavaScript was a bit tricky because I could only pass dictionaries through jsonify function in python but I only had a 9x9 matrix.
So I created a modify function that transformed the matrix into a dictionary that got as key : the cell number and as the value: the cell correct digit.

```python

    def modify(board):
    sudoku={}
    c=0
    for i in range(9):
        for j in range(9):
            sudoku[c]=board[i][j]
            c=c+1
    return sudoku

```

Then, in JavaScript I got the information through AJAX method that allows me to update the sudoku async without refreshing the page. In HTML, I created a 9x9 table and I asign the values from the dictionary that I got from Python to each corresponding cell and then I set the visibility attribute to hidden to some of the cells.

## Highlight Function
In the highlight function in Javascript I am highlighting the row, the column and the block of the selected cell with purple and also highlight the cells that have the same value with blue.
This function helps the user to resolve the puzzle easily.
![Highlight](https://scontent.fsbz3-1.fna.fbcdn.net/v/t39.30808-6/320977039_846373413079531_2027161656144748359_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=730e14&_nc_ohc=bLawgDBhQyUAX9-w2Ky&tn=pQW0bLNRdFc52eMd&_nc_ht=scontent.fsbz3-1.fna&oh=00_AfBxv2m_EDWkDs3SMXSbliY6s0ev7ssWfUPBpVWNsub7XQ&oe=63A656CD)
</hr>
Also this function remembers the selected cell that is forward use in checking if you guessed the correct digit or using the hint function.
The hint function works by setting the visibility to visible of the selected cell.
If you used the hint function 3 times, the button is disabled.
The numpad works by checking if the cell value is equal to the button value.If so,the digit will be placed in the cell, and else, one life will be taken from the 5 that you are given at the beginning of the game.If all 5 lives are gone , you will receive a message that you lost and then a new game will start.
This is how the code looks for each numpad button and hint button:


```javascript

    var numpad1=document.getElementById('numpad_num1');
        numpad1.addEventListener("click", function(){
          if(af==true)
          {
             if(was==true)
            {
              contornums=0;
              was=false;
            }
            var id_button=same.id;
            let lengthi=id_button.length;
            if (lengthi==6)
            {
              var idno=id_button.slice(-1);
            }
            else{
              var idno = id_button.slice(-2);
            }
            var id_but =parseInt(idno);
            if ((same.style.visibility=="hidden" || same.value=="")){
              if(values[id_but]==1)
              {
                same.value = 1;
                same.style.visibility = "visible";
                var cont=0;
                for (let i=0; i<=80; i++)
                {
                  var dt="cell-"+i;
                  var dt0= document.getElementById(dt);
                  if(dt0.value==values[id_but])
                  {
                    dt0.className = 'highlight2';
                  }
                  if(dt0.value==1 && dt0.style.visibility=="visible")
                  {
                    cont=cont+1;
                  }
                }
                if(cont==9)
                {
                  numpad1.style.opacity="0";
                  clear();
                }
              }
              else{
                contornums=contornums+1;
                var lifetext="life"+contornums;
                document.getElementById(lifetext).style.opacity="0";
                console.log(contornums);
              }

              if(contornums==5)
              {
                setTimeout(() => {   alert("You have lost the game!");}, 100);
                generatesudoku();
              }
            }
            af=false;
          }
        var r=0;
        for (let i=0; i<=80; i++)
        {
          var dt="cell-"+i;
          var dt0= document.getElementById(dt);
          if(dt0.style.visibility=="visible" && dt0.value!="")
          {
            r=r+1;
          }
        }
        if(win==false)
        {
          if(r==81)
          {
            setTimeout(() => {   alert("You won the game!");}, 100);
            win=true;
            generatesudoku();
          }
        }
          });


```
Firstly, we add an event listener to each of the numpad buttons. Then if a numpad button is clicked, we take the id of the selected cell(if the cell is due to be completed and not already completed), we transform it into int value and then we check to see if the dictionary(that we got through AJAX from Python) value corresponding to that id is equal to the numpad digit. If so, we place the digit in the cell, otherwise, one life is lost. We also do other checkings such as checking if we are done with one digit and used it 9 times or checking if the sudoku is completed and solved.

</hr>
The solve function sets all the cells visibility attribute to visible!

## /templates
- index.html: It's the home page from which you can acces the rules page and the sudoku page. In this page I used advanced CSS animations that I learned on Youtoube.
- layout.html: It's the layout for all the pages.
- play.html: It's the main part of the project:the game, the sudoku grid, the sudoku generator, hint button , numpad, solve button, timer...
- rules.html: It's a page that explains all the rules you need to know for playing Sudoku.

## /static
In the static folder I got all the images that I used in this project such as backgrounds, life image, hint image, numbers images..</hr>
In the static folder I also got 3 styles.css files which helped me a lot to style the app. I used a lot of animations (that I learned /or found on the internet), for example:
- the home page moving numbers in the background
- the modern buttons from all pages
- the blinking rules headings from rules page
- the moving title from home page
