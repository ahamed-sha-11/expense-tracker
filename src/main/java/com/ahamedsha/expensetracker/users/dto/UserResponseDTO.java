package com.ahamedsha.expensetracker.users.dto;

import com.ahamedsha.expensetracker.users.model.User;
import lombok.Data;

@Data
public class UserResponseDTO {
    private Long id;
    private String email;
    private String username;

    public UserResponseDTO(User user) {
        this.id = user.getId();
        this.email = user.getEmail();
        this.username = user.getUsername();
    }
}