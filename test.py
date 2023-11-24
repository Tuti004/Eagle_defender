def main_loop(self):
    running = True
    selected_block = None
    message_timer = 0
    eagle_row = 5  # Coordenada X inicial del águila
    eagle_col = 2  # Coordenada Y inicial del águila

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Bloquea la colocación de bloques si el turno del defensor ha terminado
                if self.defender_turn_over:
                    continue

                x, y = event.pos
                fila = (x - self.POS_X_MARCO) // self.CELDA
                columna = (y - self.POS_Y_MARCO) // self.CELDA

                # Obtenga las coordenadas absolutas del bloque
                bloque_x = fila * self.CELDA + self.POS_X_MARCO
                bloque_y = columna * self.CELDA + self.POS_Y_MARCO

                # Verifique si el bloque estará dentro del marco
                if not self.es_dentro_del_marco(bloque_x, bloque_y):
                    continue

                # Comprueba si las coordenadas están dentro del rango
                if 0 <= fila < self.NUM_CELDAS and 0 <= columna < self.NUM_CELDAS:
                    if self.matriz_celdas[fila][columna]:  # Si hay un bloque, lo quitamos
                        self.inventory_defender.return_block(self.matriz_celdas[fila][columna])
                        self.matriz_celdas[fila][columna] = None
                    else:  # Intentamos agregar un nuevo bloque
                        if selected_block and self.inventory_defender.use_block(selected_block):
                            self.matriz_celdas[fila][columna] = selected_block
                        else:
                            message_timer = 100

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.is_paused = not self.is_paused
                    if self.is_paused:
                        self.draw_pause_window()  # Dibuja la ventana de pausa al pausar el juego
                    else:
                        # Código para cerrar la ventana de pausa si es necesario
                        pass

                if self.defender_turn_over:
                    # Bloquea el movimiento y la selección de bloques si el turno del defensor ha terminado
                    continue
                if event.key == pygame.K_1:
                    selected_block = "concreto"
                elif event.key == pygame.K_2:
                    selected_block = "madera"
                elif event.key == pygame.K_3:
                    selected_block = "acero"
                elif event.type == pygame.KEYDOWN:
                    new_row = eagle_row
                    new_col = eagle_col
                    if event.key == pygame.K_UP:
                        new_row -= 1
                    elif event.key == pygame.K_DOWN:
                        new_row += 1
                    elif event.key == pygame.K_LEFT:
                        new_col -= 1
                    elif event.key == pygame.K_RIGHT:
                        new_col += 1
                    # Comprueba si el nuevo cuadro está vacío antes de mover el águila
                    if (0 <= new_row < self.NUM_CELDAS and
                            0 <= new_col < self.NUM_CELDAS and
                            not self.cuadro_ocupado(new_row, new_col) and
                            self.es_dentro_del_marco(self.POS_X_MARCO + new_col * self.CELDA,
                                                     self.POS_Y_MARCO + new_row * self.CELDA)):
                        eagle_row = new_row
                        eagle_col = new_col
                if event.key == pygame.K_RETURN:
                    self.show_confirmation_screen()
                    self.turn_timer_expired = True
            elif self.turn_timer_expired == True:
                pass

        self.screen.fill((255, 255, 255))  # Llena la pantalla de blanco
        fondojuego = pygame.image.load("assets/fondojuego.png")
        self.screen.blit(fondojuego, (0, 0))
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.timer_start
        remaining_time = max(0, self.timer_duration - elapsed_time)
        minutes, seconds = divmod(remaining_time // 1000, 60)

        self.dibujar_cuadricula()
        self.dibujar_imagenes()
        self.draw_player_info()
        pause_button_rect = self.draw_pause_button()

        if self.is_paused:
            resume_button_rect, quit_button_rect = self.draw_pause_window()
            pause_start_time = pygame.time.get_ticks()
            pygame.display.flip()  # Actualiza la pantalla para mostrar la ventana de pausa

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if resume_button_rect.collidepoint(event.pos):
                        self.is_paused = False  # Resumen del juego
                        self.timer_start += pygame.time.get_ticks() - pause_start_time
                    elif quit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

        # Render and display the timer on the screen
        font = pygame.font.Font(None, 36)
        timer_text = font.render(f"Time: {minutes:02}:{seconds:02}", True, (0, 0, 0))
        timer_rect = timer_text.get_rect(center=(self.screen.get_width() // 2, 30))
        self.screen.blit(timer_text, timer_rect)

        if self.defender_turn_over:

            global bailabilidad_label
            global acustica_label
            global tempo_label
            global popularidad_label
            global extra_agua

            if remaining_time <= self.timer_duration // 2 and not self.half_time_text_displayed:
                # Pausar el tiempo
                pause_start_time = pygame.time.get_ticks()
                self.is_paused = True

                self.attacker_inventory.adjust_water_bullets(extra_agua)

                print("Cantidad de balas de agua extra " + str(self.attacker_inventory.bullet_types["agua"]))

                dynamic_text = f"Beneficio Foráneo! \n Bailabilidad: {str(bailabilidad_label)}\nAcústica: {str(acustica_label)}\nTempo: {str(tempo_label)}\nPopularidad: {str(popularidad_label)}\n Balas de agua extra: {str(extra_agua)}"

                half_time_font = pygame.font.Font(None, 48)
                half_time_text = half_time_font.render(dynamic_text, True, (255, 0, 0))

                # Dividir el texto en líneas individuales
                lines = dynamic_text.split('\n')

                # Obtener la altura de cada línea de texto
                line_height = half_time_text.get_height()

                # Calcular la altura total del bloque de texto
                total_height = len(lines) * line_height

                # Calcular la posición y mostrar cada línea por separado
                for i, line in enumerate(lines):
                    text_surface = half_time_font.render(line, True, (255, 0, 0))
                    text_rect = text_surface.get_rect(
                        center=(self.screen.get_width() // 2,
                                self.screen.get_height() // 2 - total_height // 2 + i * line_height))
                    self.screen.blit(text_surface, text_rect)

                pygame.display.flip()  # Actualizar la pantalla para mostrar el texto
                pygame.time.delay(10000)  # Esperar 5 segundos
                self.half_time_text_displayed = True

                # Reanudar el tiempo después de mostrar el mensaje
                self.is_paused = False
                self.timer_start += pygame.time.get_ticks() - pause_start_time