#include "InterfaceA.h"

#ifndef PROGRAM_H
#define PROGRAM_H

#include <iostream>
using namespace std;

namespace Program {
    class Program {
    public:
        Program();
        ~Program();
        void run();
    private:
        InterfaceA a;
        InterfaceB b;

    };
}

#endif
```
```python
from abc import ABC, abstractmethod

class InterfaceA(ABC):
    @abstractmethod
    def init(self):
        pass

class Program:
    def __init__(self, a):
        self.a = a

def run():
    print("Program is running.")

a = InterfaceA()
b = InterfaceB()

# Mock for the program class
class ProgramMock(Program):
    def __init__(self, a):
        super().__init__()
        self.a = a

    def init(self):
        pass

program = ProgramMock(a)
run()
