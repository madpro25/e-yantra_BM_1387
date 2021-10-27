def chkPalindrome(s):
    c = 0
    while c < len(s):
        if s[c] != s[len(s)-c-1]:
            return "It is not a palindrome"
        c += 1

    return "It is a palindrome"


n = int(input("Enter no. of test cases: "))
i = 0
while i < n:
    print(chkPalindrome(input().lower()))
    i += 1
