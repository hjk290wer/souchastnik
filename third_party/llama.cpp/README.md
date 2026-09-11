# llama.cpp dependency

This directory is intentionally tracked as a placeholder in the repository mirror used for CI.

The native Android build requires a full `llama.cpp` checkout at the revision recorded in
`tools/llama-cpp-pin.txt`. Local development should populate this directory with that checkout.

CI must materialize the pinned dependency before invoking CMake.
