/*
 * Copyright 2015 FUJITSU LIMITED
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the License for the specific language governing permissions and limitations under
 * the License.
 */
package monasca.common.hibernate.db;

import java.io.Serializable;

import javax.persistence.Column;
import javax.persistence.Embeddable;
import javax.persistence.EnumType;
import javax.persistence.Enumerated;

import monasca.common.model.alarm.AlarmState;

@Embeddable
public class AlarmActionId implements Serializable {

  @Column(name = "alarm_definition_id", length = 36)
  private String alarm_definition_id;

  @Column(name = "alarm_state")
  @Enumerated(EnumType.STRING)
  private AlarmState alarm_state;

  @Column(name = "action_id", length = 36, nullable = false)
  private String action_id;

  public AlarmActionId() {
    super();
  }

  public AlarmActionId(String alarm_definition_id, AlarmState alarm_state, String action_id) {
    super();
    this.alarm_definition_id = alarm_definition_id;
    this.alarm_state = alarm_state;
    this.action_id = action_id;
  }

  public String getAlarm_definition_id() {
    return alarm_definition_id;
  }

  public void setAlarm_definition_id(String alarm_definition_id) {
    this.alarm_definition_id = alarm_definition_id;
  }

  public AlarmState getAlarm_state() {
    return alarm_state;
  }

  public void setAlarm_state(AlarmState alarm_state) {
    this.alarm_state = alarm_state;
  }

  public String getAction_id() {
    return action_id;
  }

  public void setAction_id(String action_id) {
    this.action_id = action_id;
  }

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = 1;
    result = prime * result + ((action_id == null) ? 0 : action_id.hashCode());
    result = prime * result + ((alarm_definition_id == null) ? 0 : alarm_definition_id.hashCode());
    result = prime * result + ((alarm_state == null) ? 0 : alarm_state.hashCode());
    return result;
  }

  @Override
  public boolean equals(Object obj) {
    if (this == obj)
      return true;
    if (obj == null)
      return false;
    if (getClass() != obj.getClass())
      return false;
    AlarmActionId other = (AlarmActionId) obj;
    if (action_id == null) {
      if (other.action_id != null)
        return false;
    } else if (!action_id.equals(other.action_id))
      return false;
    if (alarm_definition_id == null) {
      if (other.alarm_definition_id != null)
        return false;
    } else if (!alarm_definition_id.equals(other.alarm_definition_id))
      return false;
    if (alarm_state != other.alarm_state)
      return false;
    return true;
  }
}
