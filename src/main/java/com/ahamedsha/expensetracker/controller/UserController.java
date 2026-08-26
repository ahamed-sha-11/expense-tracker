package com.ahamedsha.expensetracker.controller;

import com.ahamedsha.expensetracker.dto.UserRequestDTO;
import com.ahamedsha.expensetracker.dto.UserResponseDTO;
import com.ahamedsha.expensetracker.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class UserController {

    @Autowired
    private UserService userService;

    @GetMapping("/api/users/{id}")
    public ResponseEntity<UserResponseDTO> getAllUsers(@PathVariable long id) {
        UserResponseDTO user = new UserResponseDTO(userService.findById(id));
        return ResponseEntity.ok(user);
    }

    @PostMapping("/api/users")
    public ResponseEntity<UserResponseDTO> addUser(@RequestBody UserRequestDTO user){
        UserResponseDTO userResponseDTO = new UserResponseDTO(userService.addUser(user));
        return ResponseEntity.ok(userResponseDTO);
    }

    @PostMapping("/api/users/{id}")
    public ResponseEntity<UserResponseDTO> updateUser(@PathVariable long id, @RequestBody UserRequestDTO user){
        UserResponseDTO userResponseDTO = new UserResponseDTO(userService.updateUser(user));
        return ResponseEntity.ok(userResponseDTO);
    }
}
