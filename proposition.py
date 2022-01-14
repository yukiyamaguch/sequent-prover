"""
definition

PROPOSITION: 基底クラス
ATOM: 原子命題, PROPOSITIONを継承, 変数varに制限はないが基本的に文字列
NEG: negation, PROPOSITIONを継承, 変数propはPROPOSITION
OR: or, PROPOSITIONを継承, 変数lprop,rpropはPROPOSITION
AND: and, PROPOSITIONを継承, 変数lprop,rpropはPROPOSITION
IMPL: implication, PROPOSITIONを継承, 変数lprop,rpropはPROPOSITION
"""

# 命題親クラス
class PROPOSITION ( object ):
    def __init__( self ):
        pass

# 原子命題クラス
class ATOM ( PROPOSITION ):
    def __init__ ( self, var ):
        self.var = var

    def __eq__ ( self, other ):
        if isinstance( other, ATOM ):
            return self.var == other.var
        else: return False

    def __str__ ( self ):
        #return "["+str(self.var)+"]"
        return " "+str(self.var)+" "


# 否定命題クラス
class NEG ( PROPOSITION ):
    def __init__ ( self, prop ):
        if not isinstance( prop, PROPOSITION ):
            raise Exception( "Not PROPOSITION input to NEG." )
        self.term = prop

    def __eq__ ( self, other ):
        if isinstance( other, NEG ):
            return self.term == other.term
        else: return False

    def __str__ ( self ):
        #return "[NEG, "+str(self.term)+"]"
        return "-"+str(self.term)+""

# 選言命題クラス
class OR ( PROPOSITION ):
    def __init__ ( self, lprop, rprop ):
        if not (isinstance( lprop, PROPOSITION ) \
                and isinstance( rprop, PROPOSITION )):
            raise Exception( "Not PROPOSITION input to OR." )
        self.lterm = lprop
        self.rterm = rprop

    def __eq__ ( self, other ):
        if isinstance( other, OR ):
            return self.lterm == other.lterm and self.rterm == other.rterm
        else: return False

    def __str__ ( self ):
        #return "[OR, "+str(self.lterm)+", "+str(self.rterm)+"]"
        return "("+str(self.lterm)+" v "+str(self.rterm)+")"

# 連言命題クラス
class AND ( PROPOSITION ):
    def __init__ ( self, lprop, rprop ):
        if not (isinstance( lprop, PROPOSITION ) \
                and isinstance( rprop, PROPOSITION )):
            raise Exception( "Not PROPOSITION input to AND." )
        self.lterm = lprop
        self.rterm = rprop

    def __eq__ ( self, other ):
        if isinstance( other, AND ):
            return self.lterm == other.lterm and self.rterm == other.rterm
        else: return False

    def __str__ ( self ):
        #return "[AND, "+str(self.lterm)+", "+str(self.rterm)+"]"
        return "("+str(self.lterm)+" ^ "+str(self.rterm)+")"

# 含意命題クラス
class IMPL ( PROPOSITION ):
    def __init__ ( self, lprop, rprop ):
        if not (isinstance( lprop, PROPOSITION ) \
                and isinstance( rprop, PROPOSITION )):
            raise Exception( "Not PROPOSITION input to IMPL." )
        self.lterm = lprop
        self.rterm = rprop

    def __eq__ ( self, other ):
        if isinstance( other, IMPL ):
            return self.lterm == other.lterm and self.rterm == other.rterm
        else: return False

    def __str__ ( self ):
        #return "[IMPL, "+str(self.lterm)+", "+str(self.rterm)+"]"
        return "("+str(self.lterm)+" -> "+str(self.rterm)+")"


