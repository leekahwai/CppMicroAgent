#ifndef SAMPLE_APP_H
#define SAMPLE_APP_H

#include <iostream>

namespace sample_app {
    namespace gui {
        void run();
    }
}

#endif // SAMPLE_APP_H
```

### Explanation:

1. **#pragma once**: This directive tells the compiler that the following header file can be included at one time without repeating itself. It is used here to create a mock for the `Program.h` source file.

2. **namespace sample_app::gui**: The namespace "sample_app" is made visible as it references the `gui` namespace, which contains the `run` function.

3. **void run()**: This function should be implemented within the `SampleApp.cpp` file using the standard C++ syntax for a function that runs an application.

### SampleApp.h

```cpp
#ifndef SAMPLE_APP_H
#define SAMPLE_APP_H

#include <iostream>

namespace sample_app {
    namespace gui {
        void run();
    }
}

#endif // SAMPLE_APP_H
```

This mock header defines two namespaces: `sample_app` and `gui`. The `SampleApp.cpp` file should be updated to include the following function:

```cpp
// SampleApp.cpp : Defines the entry point for the application.
//

#include "Program.h"

using namespace sample_app::gui;

using namespace sample_app::gui;
namespace gui {
    void run() {
        // Implement your application's logic here...
    }
}
```

### Compilation and Execution

- **SampleApp.cpp**: When you compile `SampleApp.cpp`, it should link against the `Program.h` file.
  
  ```sh
  g++ -o SampleApp SampleApp.cpp Program.h -lpthreads
  ```

- **Program.h**: This is a mock header that contains a function definition.

- **SampleApp.h**: This defines a namespace and references a function in `Program.h`.

- **SampleApp.cpp**: The main application logic. Replace the actual code with your C++ program.

