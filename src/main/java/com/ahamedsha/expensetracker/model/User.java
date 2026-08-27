package com.ahamedsha.expensetracker.model;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Builder
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "users", uniqueConstraints = @UniqueConstraint(columnNames = {"email"}))
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private long id;

    @Column(unique = true,  nullable = false)
    private String email;

    @Column(nullable = false)
    private String username;

    @Column(nullable = false)
    private String password;
}
