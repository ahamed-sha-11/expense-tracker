package com.ahamedsha.expensetracker.users.controller;

import com.ahamedsha.expensetracker.users.dto.UserRequestDTO;
import com.ahamedsha.expensetracker.users.dto.UserResponseDTO;
import com.ahamedsha.expensetracker.users.service.UserService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("{id}")
    public ResponseEntity<UserResponseDTO> getUser(@PathVariable long id) {
        UserResponseDTO user = new UserResponseDTO(userService.findById(id));
        return ResponseEntity.ok(user);
    }

    @PostMapping
    public ResponseEntity<UserResponseDTO> addUser(@RequestBody UserRequestDTO user){
        UserResponseDTO userResponseDTO = new UserResponseDTO(userService.addUser(user));
        return ResponseEntity.status(HttpStatus.CREATED).body(userResponseDTO);
    }

    @PatchMapping("{id}")
    public ResponseEntity<UserResponseDTO> updateUser(@PathVariable long id, @RequestBody UserRequestDTO user){
        UserResponseDTO userResponseDTO = new UserResponseDTO(userService.updateUser(id, user));
        return ResponseEntity.ok(userResponseDTO);
    }
}
