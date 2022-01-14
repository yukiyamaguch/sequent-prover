"""
Sequentデータ構造を表現するSEQUENTクラス
lsは左辺の命題列であり、rsが右辺である。
メンバのls_atom,ls_lcはそれぞれ原子命題のリストと
論理結合子を含んだ命題のリストを表す。右辺も同様。
メソッドについては、
is_atomicは論理結合子を含む命題が存在しないときに真となる述語。
is_initialは左右に等価な原子命題が存在するときに真となる述語。
get_upper_sequentは、SequentのDecomposition Rulesに従い、
変形規則の上側のSequentを出力する関数で、その際、
使用した変形規則も文字列でタプルとして出力する。

is_provable関数は入力されたSequentが証明可能であるかの述語。
再帰的に上側のSequentがinitialかどうかを確認し、全てinitialであれば真。

print_proof_figure関数は、入力されたSequentについて、
Provableであれば、証明木をアスキーアートでprintする。
"""
from proposition import *


# Sequentクラス
class SEQUENT(object):
    def __init__(self, ls, rs):
        for l in ls:
            if not isinstance(l, PROPOSITION): raise Exception("SEQUENT: input must be proposition.")
        for r in rs:
            if not isinstance(r, PROPOSITION): raise Exception("SEQUENT: input must be proposition.")
        self.ls_lc   = [l for l in ls if type(l) != ATOM]   # 左でlogical connectiveを持つ命題のリスト
        self.ls_atom = [l for l in ls if type(l) == ATOM]   # 左でlogical connectiveを持たない命題のリスト
        self.ls      = self.ls_atom + self.ls_lc    # 左の命題のリスト
        self.rs_lc   = [r for r in rs if type(r) != ATOM]   # 右でlogical connectiveを持つ命題のリスト
        self.rs_atom = [r for r in rs if type(r) == ATOM]   # 右でlogical connectiveを持たない命題のリスト
        self.rs      = self.rs_atom + self.rs_lc    # 右の命題のリスト

    def __str__(self):  # SEQUENTオブジェクトをprintしたときの出力
        string = []
        if len(self.ls) == 0:
            string.append(" ")
        else:
            for i in range(len(self.ls)-1):
                string.append(str(self.ls[i])+",")
            string.append(str(self.ls[len(self.ls)-1]))
        string.append(" ==> ")
        if len(self.rs) == 0:
            string.append(" ")
        else:
            for i in range(len(self.rs)-1):
                string.append(str(self.rs[i])+",")
            string.append(str(self.rs[len(self.rs)-1]))
        return "".join(string)

    def is_atomic ( self ): # シーケントの左と右にlogical connectiveがなければTrue
        """
        If Sequent's lprop, rprop have no logical connective, then True
        """
        if len(self.ls_lc)==0 and len(self.rs_lc)==0: return True
        return False

    def is_initial ( self ):    # シーケントの左と右に同じATOM命題があればTrue
        """
        If Sequent is initial sequent, then True
        """
        if not self.is_atomic(): return False
        for l in self.ls_atom:
            if l in self.rs_atom: return True
        return False

    def get_upper_sequent ( self ):     # シーケントのDecompositionルールによる変換, 後ろについてる文字列は表示用
        """
        If Sequent is not atomic, then return sequents with transform 1 logical connective.
        """
        if self.is_atomic(): return [], ""
        if len(self.ls_lc) != 0:
            # L-NEG
            if type(self.ls_lc[0]) == NEG :
                return [SEQUENT(self.ls_lc[1:]+self.ls_atom, self.rs+[self.ls_lc[0].term])], "-L"
            # L-AND
            if type(self.ls_lc[0]) == AND :
                return [SEQUENT(self.ls_lc[1:]+self.ls_atom+[self.ls_lc[0].lterm, self.ls_lc[0].rterm], self.rs)], "^L"
            # L-OR
            if type(self.ls_lc[0]) == OR  :
                return [SEQUENT(self.ls_lc[1:]+self.ls_atom+[self.ls_lc[0].lterm], self.rs), \
                        SEQUENT(self.ls_lc[1:]+self.ls_atom+[self.ls_lc[0].rterm], self.rs)], "vL"
            # L-IMPL
            if type(self.ls_lc[0]) == IMPL:
                return [SEQUENT(self.ls_lc[1:]+self.ls_atom, self.rs+[self.ls_lc[0].lterm]), \
                        SEQUENT(self.ls_lc[1:]+self.ls_atom+[self.ls_lc[0].rterm], self.rs)], "->L"
            raise Exception("get_upper_sequent L.")
        if len(self.rs_lc) != 0:
            # R-NEG
            if type(self.rs_lc[0]) == NEG :
                return [SEQUENT(self.ls+[self.rs_lc[0].term], self.rs_lc[1:]+self.rs_atom)], "-R"
            # R-AND
            if type(self.rs_lc[0]) == AND :
                return [SEQUENT(self.ls, self.rs_lc[1:]+self.rs_atom+[self.rs_lc[0].lterm]), \
                        SEQUENT(self.ls, self.rs_lc[1:]+self.rs_atom+[self.rs_lc[0].rterm])], "^R"
            # R-OR
            if type(self.rs_lc[0]) == OR  :
                return [SEQUENT(self.ls, self.rs_lc[1:]+self.rs_atom+[self.rs_lc[0].lterm, self.rs_lc[0].rterm])], "vR"
            # R-IMPL
            if type(self.rs_lc[0]) == IMPL:
                return [SEQUENT(self.ls+[self.rs_lc[0].lterm], self.rs_lc[1:]+self.rs_atom+[self.rs_lc[0].rterm])], "->R"
            raise Exception("get_upper_sequent R.")
        raise Exception("get_upper_sequent.")


# 入力されたSequentが証明可能であるかの述語
def is_provable ( seq ):
    """
    If Sequent is provable, then True
    """
    if seq.is_atomic():
        if seq.is_initial(): return True
        else: return False
    upper_sequents, _ = seq.get_upper_sequent()
    if len(upper_sequents) == 1:
        return is_provable(upper_sequents[0])
    if len(upper_sequents) == 2:
        return is_provable(upper_sequents[0]) and is_provable(upper_sequents[1])
    raise Exception("is_provable.")


# 入力されたSequentが証明可能ならば証明木を表示する。
# 証明可能でないならばNot Provableを表示
def print_proof_figure ( seq ):
    """
    print proof figure of input sequent.
    """
    if not is_provable(seq):
        print("Not Provable.")
        return
    sequents, lc = seq.get_upper_sequent()
    proof_figure = [str(seq)+ " ["+lc+"] "]
    while ( not len(sequents) == 0 ):
        next_sequents = []
        string = ""
        line = ""
        for s in sequents:
            ns, lc = s.get_upper_sequent()
            next_sequents += ns
            temp=None
            if lc == "": temp = str(s)+" "
            else: temp = str(s)+" ["+lc+"] "
            line+="-"*(len(temp)-1)+" "
            string+=temp
        proof_figure.append(line)
        proof_figure.append(string)
        sequents = next_sequents
    for string in proof_figure[::-1]:
        print(string)

