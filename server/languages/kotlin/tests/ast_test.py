from server.kotlin.kotlin_ast import get_ast

if __name__ == '__main__':
    code1 = """fun main() {
     val emails = listOf(
         Email("Hey! If you really want to enlarge your ML scores click here", isSpam = true),
         Email("Earn 50 more points for ML just by visiting this site!", isSpam = true),
         Email("Still have F grade? Professional help with ML right here", isSpam = true),
 
         Email("Hey, I left my phone at home. Email me if you need anything.", isSpam = false),
         Email("Stay At Home: COVID-19 news", isSpam = false),
         Email("Please see attachment for notes on today's meeting.", isSpam = false),
         Email("JetBrains license certificate", isSpam = false),
         Email("Your Education Pack expires soon ", isSpam = false)
     )
     val nbc = emails.toNaiveBayesClassifier(
         featuresSelector = { it.message.splitWords().toSet() },
         categorySelector = { it.isSpam }
     )
 
     val spamInput = "your grade is still so bad, but I can help you to get more scores".splitWords().toSet()
     require(nbc.predict(spamInput) == true) { spamInput }
 
     val legitInput = "Thank you for placing the order ".splitWords().toSet()
     require(nbc.predict(legitInput) == false) { legitInput }
 }"""
    code2 = "val a = 2+2*2"
    code3 = """val a = \"\"\" ... ${\'$\'}eq ... \"\"\""""
    print(code3)
    print(get_ast(code3))
