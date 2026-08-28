package com.ahamedsha.expensetracker.users.controller;

import com.ahamedsha.expensetracker.users.dto.UserDTOs;
import com.ahamedsha.expensetracker.users.service.UserService;
import jakarta.validation.Valid;
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

    @GetMapping("/{id}")
    public ResponseEntity<UserDTOs.Response> getUser(@PathVariable long id) {
        return ResponseEntity.ok(UserDTOs.Response.from(userService.findById(id)));
    }

    @PostMapping
    public ResponseEntity<UserDTOs.Response> addUser(@Valid @RequestBody UserDTOs.Create request) {
        UserDTOs.Response body = UserDTOs.Response.from(userService.addUser(request));
        return ResponseEntity.status(HttpStatus.CREATED).body(body);
    }

    @PatchMapping("/{id}")
    public ResponseEntity<UserDTOs.Response> updateUser(@PathVariable long id,
            @Valid @RequestBody UserDTOs.Update request) {
        return ResponseEntity.ok(UserDTOs.Response.from(userService.updateUser(id, request)));
    }
}