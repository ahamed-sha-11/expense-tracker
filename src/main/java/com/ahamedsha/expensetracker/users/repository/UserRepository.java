package com.ahamedsha.expensetracker.users.repository;


import com.ahamedsha.expensetracker.users.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
}
