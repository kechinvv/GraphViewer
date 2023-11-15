from server.java.java_ast import get_ast

if __name__ == '__main__':
    code1 = """
    public class A extends B {
        @Override
        public void upsert(BaseEntry<MemorySegment> entry) {
            State currentState = state;
    
            lock.readLock().lock();
            try {
                currentState.memory.put(entry);
            } finally {
                lock.readLock().unlock();
            }
    
            try {
                if (currentState.memory.getBytesSize() >= config.flushThresholdBytes()) {
                    flush();
                }
            } catch (IOException e) {
                throw new UncheckedIOException(e);
            }
        }
    }
    """
    code2 = """
        class Example{
            public static void main(){
                int a;
                a = 5;
            }
        }
    """
    code3 = """
    class A {
        public static void main() {
            List<Emails> emails = Arrays.of(
                new Email("Hey! If you really want to enlarge your ML scores click here", isSpam = true),
                new Email("Earn 50 more points for ML just by visiting this site!", isSpam = true),
                new Email("Still have F grade? Professional help with ML right here", isSpam = true),
                
                new Email("Hey, I left my phone at home. Email me if you need anything.", isSpam = false),
                new Email("Stay At Home: COVID-19 news", isSpam = false),
                new Email("Please see attachment for notes on today's meeting.", isSpam = false),
                new Email("JetBrains license certificate", isSpam = false),
                new Email("Your Education Pack expires soon ", isSpam = false)
            );
            
            NBC nbc = toNativeBayesClassifier(
                emails
            );
            
            String spamInput = "your grade is still so bad, but I can help you to get more scores".splitWords().toSet();
            require(nbc.predict(spamInput) == true);
            
            String legitInput = "Thank you for placing the order ".splitWords().toSet();
            require(nbc.predict(legitInput) == false);
        }
    }
    """
    code4 = """
    public class A extends B {
        @Override
        public void upsert(BaseEntry<MemorySegment> entry) {
            State currentState = state;
    
            lock.readLock().lock();
            try {
                currentState.memory.put(entry);
            } finally {
                lock.readLock().unlock();
            }
    
            try {
                if (currentState.memory.getBytesSize() >= config.flushThresholdBytes()) {
                    flush();
                }
            } catch (IOException e) {
                throw new UncheckedIOException(e);
            }
        }
        
        public static void main(){
            int a;
            a = 5;
        }
    }
    
    class Example{
        public static void main(){
            int a;
            a = 5 ^ 2;
        }
    }
    """
    print(code4)
    print(get_ast(code4))
