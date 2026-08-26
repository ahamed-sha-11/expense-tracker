package com.ahamedsha.expensetracker.service;

import com.ahamedsha.expensetracker.dto.UserRequestDTO;
import com.ahamedsha.expensetracker.dto.UserResponseDTO;
import com.ahamedsha.expensetracker.model.User;
import com.ahamedsha.expensetracker.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    public List<UserResponseDTO> findAll() {
        return null;
    }

    public UserResponseDTO addUser(UserRequestDTO userRequestDTO) {
        User user = User.builder()
                .username(userRequestDTO.getUsername())
                .email(userRequestDTO.getEmail())
                .password(userRequestDTO.getPassword())
                .build();


        return new UserResponseDTO(userRepository.save(user));
    }
}
