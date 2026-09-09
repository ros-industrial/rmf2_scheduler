add_executable(rs_http_request rs_http_request.cpp)
target_link_libraries(rs_http_request rmf2_scheduler::rmf2_scheduler)

add_executable(ld_broker_crud ld_broker_crud.cpp)
target_link_libraries(ld_broker_crud rmf2_scheduler::rmf2_scheduler)

add_executable(create_sample_backups create_sample_backups.cpp)
target_link_libraries(create_sample_backups rmf2_scheduler::rmf2_scheduler)

add_executable(clear_ld_broker clear_ld_broker.cpp)
target_link_libraries(clear_ld_broker rmf2_scheduler::rmf2_scheduler)

add_executable(run_scheduler run_scheduler.cpp)
target_link_libraries(run_scheduler rmf2_scheduler::rmf2_scheduler)

install(TARGETS
  rs_http_request
  ld_broker_crud
  create_sample_backups
  clear_ld_broker
  run_scheduler
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/rmf2_scheduler
)
