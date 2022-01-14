"""
main.pyでは、proposition.pyで定義した命題と、
sequentProver.pyで定義したSequent、関数を用いて、
あるSequentが証明可能かを判定し、
証明可能であれば、その証明木を表示する。

以下に命題の表現の例、Sequentの表現の例、実行例を示した。
"""
from proposition import *
from sequentProver import SEQUENT
import sequentProver


# Test 1: s1 = ー＞A∨￢A (排中律)
s1 = SEQUENT([], [OR(ATOM("A"), NEG(ATOM("A")))])
print("Test 1: "+str(s1))
print("Proof Figure 1:")
sequentProver.print_proof_figure(s1)
print()

# Test2: s2 = A⇒Bー＞￢A∨B (A⇒Bと￢A∨Bは論理的等価)
s2 = SEQUENT([IMPL(ATOM("A"),ATOM("B"))], [OR(NEG(ATOM("A")), ATOM("B"))])
print("Test 2: "+str(s2))
print("Proof Figure 2:")
sequentProver.print_proof_figure(s2)
print()

# Test3: s3 = ー＞(A⇒B)⇒A (証明可能でない)
s3 = SEQUENT([], [IMPL(IMPL(ATOM("A"), ATOM("B")), ATOM("A"))])
print("Test 3: "+str(s3))
print("Proof Figure 3:")
sequentProver.print_proof_figure(s3)
print()

# Test4: s4 = ー＞A⇒(B⇒A) (トートロジーの一つ)
s4 = SEQUENT([], [IMPL(ATOM("A"), IMPL(ATOM("B"), ATOM("A")))])
print("Test 4: "+str(s4))
print("Proof Figure 4:")
sequentProver.print_proof_figure(s4)
print()

# Test5: s5 = A, A⇒B, B⇒Cー＞ C (三段論法)
s5 = SEQUENT([ATOM("A"), IMPL(ATOM("A"), ATOM("B")), IMPL(ATOM("B"), ATOM("C"))],
             [ATOM("C")])
print("Test 5: "+str(s5))
print("Proof Figure 5:")
sequentProver.print_proof_figure(s5)
print()
