# GitHubBurrito

## Description

A GitHub client implementing Rust's magical monads


## The rationale

I've had to work in the past with clients to connect, read and manipulate external resources,
and for the lack of a better term... it always was a huge pain in the butt to control all error cases, without them
bubbling up all across my codebase because of heavy Exception-based error management, resulting in potential null-cases,
bad typing, etc. 

This is no production-code, nor is it likely ever going to be. That's me fooling around and playing with monadic programming
