# FPY

## Code Snippets

### Basic Variables
Input
```haskell
let x = 1
x
```
Generated
```python
print((lambda x: x)(1))
```
Output
```txt
1
```

### Arithmethic Expressions
Input
```haskell
let x = 1
let y = 2
x + y / 4
```
Generated
```python
print((lambda x: lambda y: x + y / 4)(1)(2))
```
Output
```txt
1.5
```

### Strings
Input
```haskell
let myString = "Hello, "
myString + "World!"
```
Generated
```python
print((lambda myString: myString + "World!")("Hello, "))
```
Output
```txt
Hello, World!
```

### Lambdas
Input
```haskell
let add = &x &y x + y
add 1 2
```
Generated
```python
print((lambda add: add(1)(2))(lambda x: lambda y: x + y))
```
Output
```txt
3
```
