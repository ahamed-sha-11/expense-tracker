package com.ahamedsha.expensetracker.dto;

import com.ahamedsha.expensetracker.model.User;
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