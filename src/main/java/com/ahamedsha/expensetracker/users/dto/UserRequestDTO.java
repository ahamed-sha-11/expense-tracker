package com.ahamedsha.expensetracker.users.dto;

import lombok.Data;

@Data
public class UserRequestDTO {
    private long id;
    private String email;
    private String username;
    private String password;
}
