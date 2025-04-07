# Define constants to represent character classes
LETTER = 0        #Used when a character is a lette
#Used whe n a character is a digit (0-9).'

DIGIT = 1        
UNKNOWN = 99    #For characters we don't categorize as letters or digits (as operators)
EOF = -1         #Marks the end of  input

# Token codes ( help us identify what kind of thing we’re looking at :)
INT_LIT = 10        # Integer literal (exp: 123)
IDENT = 11          # Identifier (exp: variable names: x, total)
ASSIGN_OP = 20      # Assignment operator (=), not used here but might be as for  extensions
ADD_OP = 21         # Addition operator (+)
SUB_OP = 22         # Subtraction operator (-)
MULT_OP = 23        # Multiplication operator (*)
DIV_OP = 24         # Division operator (/)
LEFT_PAREN = 25     # Left parenthesis (
RIGHT_PAREN = 26    # Right parenthesis )

# This class handles the actual lexical analysis (tokenizing input)
class Lexer:
    def __init__(self, input_string):
        self.input = input_string          # The string we  analyze
        self.index = 0                     # Keeps track of where we are in  string
        self.charClass = None              # Class of current character (letter, digit,  ..etc)
        self.lexeme = ""                   # The current numbers  of characters we're building into a token
        self.nextChar = ''                 # The current character being processed
        self.lexLen = 0                    # Unused, but could track length of lexeme
        self.nextToken = None              # Stores the token code of the current lexeme
        self.getChar()                     # Get  first character to start

    def addChar(self):
        # Adds the current character to our lexeme (for exp: builds a token string one char at a time)
        self.lexeme += self.nextChar

    def getChar(self):
        # Reads the next character in the input and figures out what kind of character it is
        if self.index >= len(self.input):  # If gone past the input we're done
            self.charClass = EOF
            self.nextChar = ''
        else:
            self.nextChar = self.input[self.index]  # Get the next character
            self.index += 1                         # Move to the next index
            if self.nextChar.isalpha():             # If  a letter
                self.charClass = LETTER
            elif self.nextChar.isdigit():           # If a digit
                self.charClass = DIGIT
            else:                                   # If it's not a letter or digit (like +, - ...etc.)
                self.charClass = UNKNOWN

    def getNonBlank(self):
        # Skip  whitespace in the input (spaces, TABS ...etc.)
        while self.nextChar.isspace():
            self.getChar()

    def lookup(self, ch):
        # Match operators or special characters to their token types
        if ch == '(':
            self.addChar()
            self.nextToken = LEFT_PAREN
        elif ch == ')':
            self.addChar()
            self.nextToken = RIGHT_PAREN
        elif ch == '+':
            self.addChar()
            self.nextToken = ADD_OP
        elif ch == '-':
            self.addChar()
            self.nextToken = SUB_OP
        elif ch == '*':
            self.addChar()
            self.nextToken = MULT_OP
        elif ch == '/':
            self.addChar()
            self.nextToken = DIV_OP
        else:
            self.addChar()
            self.nextToken = EOF  # Not accurate but serves as a fallback
        return self.nextToken

    def lex(self):
        # This function is the heart of the lexer—it identifies one token at a time
        self.lexeme = ""              # Reset  current lexeme
        self.getNonBlank()            # Skip over spaces

        if self.charClass == LETTER:
            # If  letter then keep building identifier (may include digits too)
            self.addChar()
            self.getChar()
            while self.charClass in [LETTER, DIGIT]:
                self.addChar()
                self.getChar()
            self.nextToken = IDENT

        elif self.charClass == DIGIT:
            # If it startsdigit keep adding digits to form an integer literal
            self.addChar()
            self.getChar()
            while self.charClass == DIGIT:
                self.addChar()
                self.getChar()
            self.nextToken = INT_LIT

        elif self.charClass == UNKNOWN:
            # If unknown character  check if it's a known symbol like +, *,... etc.
            self.lookup(self.nextChar)
            self.getChar()

        elif self.charClass == EOF:
            # If reached the end of input mark the token as EOF
            self.nextToken = EOF
            self.lexeme = "EOF"

        # Show the result of  lexing step
        print(f"Next token is: {self.nextToken}, Next lexeme is {self.lexeme}")
        return self.nextToken


#  Test function to run the lexer on a sample string 
def test_lexer():
    print("=== Lexical Analysis Test ===")
    expression = "sum1 + (23 - 4) * total_3 / 2"  # Sample expression to tokenize
    lexer = Lexer(expression)                    # Create a Lexer object with the input
    while lexer.lex() != EOF:                    # Keep calling lex() until we hit EOF
        pass

# Start the test only if this file is run directly....;)
if __name__ == "__main__":
    test_lexer()

