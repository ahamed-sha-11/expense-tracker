package com.ahamedsha.expensetracker.controller;

import com.ahamedsha.expensetracker.dto.UserRequestDTO;
import com.ahamedsha.expensetracker.model.User;
import com.ahamedsha.expensetracker.dto.UserResponseDTO;
import com.ahamedsha.expensetracker.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class UserController {

    @Autowired
    private UserService userService;

    @GetMapping("/api/users")
    public ResponseEntity<List<UserResponseDTO>> getAllUsers() {
        List<UserResponseDTO> users = userService.findAll();
        return ResponseEntity.ok(users);
    }

    @PostMapping("/api/users")
    public ResponseEntity<UserResponseDTO> addUser(@RequestBody UserRequestDTO user){
        UserResponseDTO userResponseDTO = userService.addUser(user);
        return ResponseEntity.ok(userResponseDTO);
    }
}
