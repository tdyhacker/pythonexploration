
# Lazy :P
WHITE = "White"
BLACK = "Black"

blank_fn = lambda : ['' for x in range(8)]

color_fn_black = lambda : [(((x + 1) % 2) and 'B') or 'W' for x in range(8)]
color_fn_white = lambda : [((x % 2) and 'B') or 'W' for x in range(8)]

# Basic board
chess_board = {"A": blank_fn(),
               "B": blank_fn(),
               "C": blank_fn(),
               "D": blank_fn(),
               "E": blank_fn(),
               "F": blank_fn(),
               "G": blank_fn(),
               "H": blank_fn()
               }

# Color layout
chess_board_colors = {"A": color_fn_black(),
                      "B": color_fn_white(),
                      "C": color_fn_black(),
                      "D": color_fn_white(),
                      "E": color_fn_black(),
                      "F": color_fn_white(),
                      "G": color_fn_black(),
                      "H": color_fn_white()
                      }

class Piece(object):
    def __init__(self, name = "", digest = "", side = ""):
        self.name = name
        self.digest = digest
        self.side = side
    
    def __repr__(self):
        return "(%s)%s" % (self.side[0], self.digest)
        
    
    def movement(self):
        """
        Override this method with the proper information
        """
        pass
    
    def putSelfInCheck(self):
        "If I move can the King be put in check?"
        return False
    
    def isKingInCheck(self):
        "If the king is in check"
        return False

class King(Piece):
    def __init__(self, side):
        Piece.__init__(self, "King", "Ki", side)
    
    def movement(self):
        pass

class Queen(Piece):
    def __init__(self, side):
        Piece.__init__(self, "Queen", "Qu", side)
    
    def movement(self):
        pass

class Bishop(Piece):
    def __init__(self, side):
        Piece.__init__(self, "Kishop", "Bi", side)
    
    def movement(self):
        pass

class Knight(Piece):
    def __init__(self, side):
        Piece.__init__(self, "Knight", "Kn", side)
    
    def movement(self):
        pass

class Rook(Piece):
    def __init__(self, side):
        Piece.__init__(self, "Rook", "Ro", side)
    
    def movement(self):
        pass

class Pawn(Piece):
    def __init__(self, side):
        Piece.__init__(self, "Pawn", "Pa", side)
    
    def movement(self):
        pass

# Standard board setup
chess_board = {"A": [Rook(WHITE),   Pawn(WHITE), '', '', '', '', Pawn(BLACK), Rook(BLACK)],
               "B": [Knight(WHITE), Pawn(WHITE), '', '', '', '', Pawn(BLACK), Knight(BLACK)],
               "C": [Bishop(WHITE), Pawn(WHITE), '', '', '', '', Pawn(BLACK), Bishop(BLACK)],
               "D": [Queen(WHITE),  Pawn(WHITE), '', '', '', '', Pawn(BLACK), Queen(BLACK)],
               "E": [King(WHITE),   Pawn(WHITE), '', '', '', '', Pawn(BLACK), King(BLACK)],
               "F": [Bishop(WHITE), Pawn(WHITE), '', '', '', '', Pawn(BLACK), Bishop(BLACK)],
               "G": [Knight(WHITE), Pawn(WHITE), '', '', '', '', Pawn(BLACK), Knight(BLACK)],
               "H": [Rook(WHITE),   Pawn(WHITE), '', '', '', '', Pawn(BLACK), Rook(BLACK)]
               }
